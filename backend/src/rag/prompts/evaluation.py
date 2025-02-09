"""Evaluation system for prompt templates."""
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class EvaluationResult:
    """Data class for evaluation results."""

    prompt_name: str
    question: str
    answer: str
    metrics: Dict[str, float]
    metadata: Dict[str, Any]
    timestamp: str = datetime.now().isoformat()


class PromptEvaluator:
    """Evaluator for different prompt templates."""

    def __init__(self, output_dir: str = "evaluation_results"):
        """Initialize the evaluator.

        Args:
            output_dir: Directory to save evaluation results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results: List[EvaluationResult] = []

        # Legal terms patterns (common Turkish legal terms)
        self.legal_terms_patterns = [
            r"taksir",
            r"kusur",
            r"ihmal",
            r"kast",
            r"hukuka uygunluk",
            r"meşru müdafaa",
            r"zorunluluk hali",
            r"görevin ifası",
            r"hakkın kullanılması",
            r"rıza",
            r"kusur yeteneği",
            r"isnat yeteneği",
            r"teşebbüs",
            r"iştirak",
            r"içtima",
            r"zamanaşımı",
        ]

    def evaluate_response(
        self,
        prompt_name: str,
        question: str,
        answer: str,
        expected_structure: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, float]:
        """Evaluate a response based on various quality metrics.

        This method evaluates the quality of a generated answer using multiple metrics:
        - Length and content quality
        - Structural adherence to expected format
        - Legal reference usage and formatting
        - Legal terminology usage
        - Text formatting and presentation
        - Section completeness

        Args:
            prompt_name: Name of the prompt template used
            question: The original question asked
            answer: The generated answer to evaluate
            expected_structure: Optional list of expected section names
            metadata: Optional metadata containing evaluation parameters:
                - min_articles: Minimum number of article references expected
                - expected_terms: List of legal terms expected in the answer
                - complexity: Expected answer complexity ('low', 'medium', 'high')

        Returns:
            Dict[str, float]: Dictionary of evaluation metrics, including:
                - length_score: Score for answer length (0-1)
                - structure_score: Score for structural adherence (0-1)
                - legal_reference_score: Score for legal reference usage (0-1)
                - term_usage_score: Score for legal terminology usage (0-1)
                - formatting_score: Score for text formatting (0-1)
                - section_completeness: Score for section completeness (0-1)
                - overall_score: Weighted combination of all scores (0-1)
        """
        metrics = {}

        # Content length and quality metrics
        metrics["length_score"] = self._evaluate_length(answer)
        metrics["structure_score"] = (
            self._evaluate_structure(answer, expected_structure)
            if expected_structure
            else 1.0
        )

        # Legal specific metrics
        metrics["legal_reference_score"] = self._evaluate_legal_references(
            answer, min_articles=metadata.get("min_articles", 2) if metadata else 2
        )
        metrics["term_usage_score"] = self._evaluate_legal_terms(
            answer,
            expected_terms=metadata.get("expected_terms", []) if metadata else [],
        )
        metrics["formatting_score"] = self._evaluate_formatting(answer)

        # Section completeness metrics
        metrics["section_completeness"] = self._evaluate_section_completeness(
            answer,
            complexity=metadata.get("complexity", "medium") if metadata else "medium",
        )

        # Calculate overall score with weighted components
        weights = {
            "length_score": 0.1,
            "structure_score": 0.2,
            "legal_reference_score": 0.2,
            "term_usage_score": 0.2,
            "formatting_score": 0.1,
            "section_completeness": 0.2,
        }

        metrics["overall_score"] = sum(
            metrics[key] * weight for key, weight in weights.items()
        )

        return metrics

    def _evaluate_length(self, answer: str) -> float:
        """Evaluate the length and detail of the answer.

        This method scores the answer based on its length, with an ideal range
        of 300-1000 characters. Scores are calculated as follows:
        - Below 300: Linear score from 0 to 1 based on length/300
        - 300-1000: Perfect score of 1.0
        - Above 1000: Decreasing score based on excess length

        Args:
            answer: The answer text to evaluate

        Returns:
            float: Length score between 0 and 1
        """
        length = len(answer)
        if length < 300:
            return length / 300
        elif length > 1000:
            return 1.0 - ((length - 1000) / 1000)
        return 1.0

    def _evaluate_structure(self, answer: str, expected_sections: List[str]) -> float:
        """Evaluate if the answer follows the expected structure.

        Args:
            answer: Generated answer
            expected_sections: List of expected section names

        Returns:
            float: Structure score (0-1)
        """
        if not expected_sections:
            return 1.0

        found_sections = 0
        total_sections = len(expected_sections)

        for section in expected_sections:
            # Check for section headers
            if section in answer:
                found_sections += 1

            # Check for section content (at least 2 lines after header)
            section_pattern = (
                f"{section}:?(.*?)(?={expected_sections[0]}|$)"
                if expected_sections
                else ""
            )
            if section_pattern:
                match = re.search(section_pattern, answer, re.DOTALL)
                if match and len(match.group(1).strip().split("\n")) >= 2:
                    found_sections += 0.5

        return min(1.0, found_sections / (total_sections * 1.5))

    def _evaluate_legal_references(self, answer: str, min_articles: int = 2) -> float:
        """Evaluate the usage and formatting of legal references in the answer.

        This method evaluates how well legal references (TCK articles) are used and
        formatted in the answer. The score is based on:
        - Number of properly formatted article references
        - Variety in reference formats (standalone vs. inline)
        - Exceeding the minimum required references

        Args:
            answer: The answer text to evaluate
            min_articles: Minimum number of article references expected (default: 2)

        Returns:
            float: Legal reference score between 0 and 1, calculated as:
                - Base score: min(1.0, actual_refs / min_required)
                - Format bonus: 0.2 if both standalone and inline refs present
                - Excess bonus: Up to 0.2 for exceeding minimum requirement
        """
        # Count properly formatted article references
        article_refs = re.findall(r"Madde\s+\d+", answer)

        # Count inline references
        inline_refs = re.findall(r"\(Madde\s+\d+\)", answer)

        # Calculate base score based on number of references
        ref_count = len(article_refs) + len(inline_refs)
        base_score = min(1.0, ref_count / min_articles)

        # Bonus for variety in reference formats
        format_bonus = 0.2 if article_refs and inline_refs else 0.0

        # Bonus for exceeding minimum
        excess_bonus = (
            min(0.2, (ref_count - min_articles) * 0.1)
            if ref_count > min_articles
            else 0.0
        )

        return min(1.0, base_score + format_bonus + excess_bonus)

    def _evaluate_legal_terms(
        self, answer: str, expected_terms: List[str] = None
    ) -> float:
        """Evaluate the usage of legal terminology in the answer.

        This method evaluates how well legal terms are used in the answer,
        considering both expected terms and general legal terminology. The score
        is based on:
        - Usage of expected legal terms (if provided)
        - Usage of common Turkish legal terms
        - Proper definition and explanation of terms

        Args:
            answer: The answer text to evaluate
            expected_terms: Optional list of legal terms expected in the answer

        Returns:
            float: Legal terminology score between 0 and 1, calculated as:
                - General term score: min(0.5, term_count/10)
                - Expected term score: 0.5 * (found_terms/expected_terms)
                - Term definitions are weighted double
        """
        term_count = 0
        expected_term_count = 0

        # Check for expected terms if provided
        if expected_terms:
            for term in expected_terms:
                if term.lower() in answer.lower():
                    expected_term_count += 1

        # Check for general legal terms
        for pattern in self.legal_terms_patterns:
            matches = re.findall(pattern, answer.lower())
            term_count += len(matches)

        # Check for term definitions
        definitions = re.findall(r'"([^"]+)"\s*(?::|tanımı:|terimi:)\s*([^.]+)', answer)
        term_count += len(definitions) * 2  # Definitions are weighted more

        # Calculate scores
        general_term_score = min(0.5, term_count / 10)
        expected_term_score = (
            0.5 * (expected_term_count / len(expected_terms)) if expected_terms else 0.5
        )

        return general_term_score + expected_term_score

    def _evaluate_formatting(self, answer: str) -> float:
        """Evaluate the formatting and presentation quality of the answer.

        This method evaluates the use of various formatting elements that improve
        readability and structure. Points are awarded for:
        - Bold text (using **) [0.2 points]
        - Bullet points [0.2 points]
        - Numbered lists [0.2 points]
        - Proper paragraph breaks [0.2 points]
        - Consistent header capitalization [0.2 points]

        Args:
            answer: The answer text to evaluate

        Returns:
            float: Formatting score between 0 and 1, with 0.2 points for each
                  properly used formatting element
        """
        score = 0.0

        # Check for bold text
        if re.search(r"\*\*[^*]+\*\*", answer):
            score += 0.2

        # Check for bullet points
        if re.search(r"[-•]\s+\w+", answer):
            score += 0.2

        # Check for numbered lists
        if re.search(r"\d+\.\s+\w+", answer):
            score += 0.2

        # Check for paragraph breaks
        if re.search(r"\n\n", answer):
            score += 0.2

        # Check for consistent capitalization in headers
        if re.search(r"^[A-ZİĞÜŞÖÇ\s]+:", answer, re.MULTILINE):
            score += 0.2

        return score

    def _evaluate_section_completeness(
        self, answer: str, complexity: str = "medium"
    ) -> float:
        """Evaluate how complete each section is based on content length and quality.

        Args:
            answer: The generated answer to evaluate
            complexity: Expected complexity level ('low', 'medium', 'high')

        Returns:
            float: Score between 0-1 indicating section completeness
        """
        sections = ["SORU KAPSAMI", "İLGİLİ KANUN MADDELERİ", "HUKUKİ ANALİZ", "SONUÇ"]

        # Adjust minimum content length based on complexity
        min_content_length = {"low": 100, "medium": 200, "high": 300}.get(
            complexity.lower(), 200
        )

        section_scores = []
        for i, section in enumerate(sections):
            next_section = sections[i + 1] if i < len(sections) - 1 else None

            # Extract section content
            pattern = (
                f"{section}:?(.*?)(?={next_section}:|$)"
                if next_section
                else f"{section}:?(.*?)$"
            )
            match = re.search(pattern, answer, re.DOTALL)
            if not match:
                section_scores.append(0.0)
                continue

            content = match.group(1).strip()
            content_length = len(content)

            # Score based on content length
            length_score = min(1.0, content_length / min_content_length)

            # Score based on content quality indicators
            quality_indicators = [
                bool(re.search(r"\*\*[^*]+\*\*", content)),  # Bold text
                bool(re.search(r"[-•]\s+\w+", content)),  # Bullet points
                bool(re.search(r"\d+\.\s+\w+", content)),  # Numbered lists
                bool(re.search(r"Madde\s+\d+", content)),  # Legal references
                len(content.split("\n")) > 2,  # Multiple paragraphs
            ]
            quality_score = sum(
                1 for indicator in quality_indicators if indicator
            ) / len(quality_indicators)

            section_scores.append((length_score + quality_score) / 2)

        return sum(section_scores) / len(sections)

    def add_result(
        self,
        prompt_name: str,
        question: str,
        answer: str,
        metrics: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an evaluation result to the collection.

        Args:
            prompt_name: Name of the prompt template used
            question: The input question
            answer: The generated answer
            metrics: Dictionary of evaluation metrics
            metadata: Optional metadata about the evaluation
        """
        result = EvaluationResult(
            prompt_name=prompt_name,
            question=question,
            answer=answer,
            metrics=metrics,
            metadata=metadata or {},
        )
        self.results.append(result)

    def save_results(self, filename: Optional[str] = None) -> None:
        """Save evaluation results to a JSON file.

        Args:
            filename: Optional custom filename, defaults to timestamp-based name
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)

        # Convert results to serializable format
        serialized_results = [
            {
                "prompt_name": r.prompt_name,
                "question": r.question,
                "answer": r.answer,
                "metrics": r.metrics,
                "metadata": r.metadata,
                "timestamp": r.timestamp,
            }
            for r in self.results
        ]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serialized_results, f, ensure_ascii=False, indent=2)

    def load_results(self, filename: str) -> None:
        """Load evaluation results from a JSON file.

        Args:
            filename: Name of the file to load results from
        """
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.results = [EvaluationResult(**result) for result in data]

    def get_summary(self) -> Dict[str, Any]:
        """Generate a summary of evaluation results.

        Returns:
            Dict containing:
                - total_evaluations: Number of evaluations
                - average_scores: Average scores for each metric
                - prompt_performance: Performance metrics by prompt template
                - best_performing: Best performing prompt template
        """
        if not self.results:
            return {"error": "No evaluation results available"}

        summary = {
            "total_evaluations": len(self.results),
            "average_scores": {},
            "prompt_performance": {},
            "best_performing": None,
        }

        # Calculate average scores across all evaluations
        all_metrics = {}
        for result in self.results:
            for metric, value in result.metrics.items():
                if metric not in all_metrics:
                    all_metrics[metric] = []
                all_metrics[metric].append(value)

        summary["average_scores"] = {
            metric: sum(values) / len(values) for metric, values in all_metrics.items()
        }

        # Calculate performance by prompt template
        prompt_metrics = {}
        for result in self.results:
            if result.prompt_name not in prompt_metrics:
                prompt_metrics[result.prompt_name] = []
            prompt_metrics[result.prompt_name].append(result.metrics["overall_score"])

        summary["prompt_performance"] = {
            prompt: sum(scores) / len(scores)
            for prompt, scores in prompt_metrics.items()
        }

        # Identify best performing prompt
        if prompt_metrics:
            summary["best_performing"] = max(
                summary["prompt_performance"].items(),
                key=lambda x: x[1],
            )[0]

        return summary

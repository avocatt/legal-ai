"""Evaluation system for prompt templates."""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import os
import re
from datetime import datetime


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
            r"zamanaşımı"
        ]

    def evaluate_response(
        self,
        prompt_name: str,
        question: str,
        answer: str,
        expected_structure: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, float]:
        """Evaluate a response based on various metrics."""
        metrics = {}

        # Content length and quality metrics
        metrics["length_score"] = self._evaluate_length(answer)
        metrics["structure_score"] = self._evaluate_structure(
            answer, expected_structure) if expected_structure else 1.0

        # Legal specific metrics
        metrics["legal_reference_score"] = self._evaluate_legal_references(
            answer,
            min_articles=metadata.get("min_articles", 2) if metadata else 2
        )
        metrics["term_usage_score"] = self._evaluate_legal_terms(
            answer,
            expected_terms=metadata.get(
                "expected_terms", []) if metadata else []
        )
        metrics["formatting_score"] = self._evaluate_formatting(answer)

        # Section completeness metrics
        metrics["section_completeness"] = self._evaluate_section_completeness(
            answer,
            complexity=metadata.get(
                "complexity", "medium") if metadata else "medium"
        )

        # Calculate overall score with weighted components
        weights = {
            "length_score": 0.1,
            "structure_score": 0.2,
            "legal_reference_score": 0.2,
            "term_usage_score": 0.2,
            "formatting_score": 0.1,
            "section_completeness": 0.2
        }

        metrics["overall_score"] = sum(
            metrics[key] * weight
            for key, weight in weights.items()
        )

        return metrics

    def _evaluate_length(self, answer: str) -> float:
        """Evaluate the length and detail of the answer."""
        # Target length is between 300 and 1000 characters
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
            section_pattern = f"{section}:?(.*?)(?={expected_sections[0]}|$)" if expected_sections else ""
            if section_pattern:
                match = re.search(section_pattern, answer, re.DOTALL)
                if match and len(match.group(1).strip().split('\n')) >= 2:
                    found_sections += 0.5

        return min(1.0, found_sections / (total_sections * 1.5))

    def _evaluate_legal_references(self, answer: str, min_articles: int = 2) -> float:
        """Evaluate the usage and formatting of legal references."""
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
        excess_bonus = min(0.2, (ref_count - min_articles)
                           * 0.1) if ref_count > min_articles else 0.0

        return min(1.0, base_score + format_bonus + excess_bonus)

    def _evaluate_legal_terms(self, answer: str, expected_terms: List[str] = None) -> float:
        """Evaluate the usage of legal terminology."""
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
        definitions = re.findall(
            r'"([^"]+)"\s*(?::|tanımı:|terimi:)\s*([^.]+)', answer)
        term_count += len(definitions) * 2  # Definitions are weighted more

        # Calculate scores
        general_term_score = min(0.5, term_count / 10)
        expected_term_score = 0.5 * \
            (expected_term_count / len(expected_terms)) if expected_terms else 0.5

        return general_term_score + expected_term_score

    def _evaluate_formatting(self, answer: str) -> float:
        """Evaluate the formatting and presentation of the answer."""
        score = 0.0

        # Check for bold text
        if re.search(r'\*\*[^*]+\*\*', answer):
            score += 0.2

        # Check for bullet points
        if re.search(r'[-•]\s+\w+', answer):
            score += 0.2

        # Check for numbered lists
        if re.search(r'\d+\.\s+\w+', answer):
            score += 0.2

        # Check for paragraph breaks
        if re.search(r'\n\n', answer):
            score += 0.2

        # Check for consistent capitalization in headers
        if re.search(r'^[A-ZİĞÜŞÖÇ\s]+:', answer, re.MULTILINE):
            score += 0.2

        return score

    def _evaluate_section_completeness(self, answer: str, complexity: str = "medium") -> float:
        """Evaluate how complete each section is."""
        sections = [
            "SORU KAPSAMI",
            "İLGİLİ KANUN MADDELERİ",
            "HUKUKİ ANALİZ",
            "SONUÇ"
        ]

        # Adjust minimum content length based on complexity
        min_content_length = {
            "low": 100,
            "medium": 200,
            "high": 300
        }.get(complexity.lower(), 200)

        section_scores = []
        for i, section in enumerate(sections):
            next_section = sections[i + 1] if i < len(sections) - 1 else None

            # Extract section content
            pattern = f"{section}:?(.*?)(?={next_section}:|$)" if next_section else f"{section}:?(.*?)$"
            match = re.search(pattern, answer, re.DOTALL)

            if match:
                content = match.group(1).strip()

                # Score based on content length and complexity
                length_score = min(1.0, len(content) / min_content_length)

                # Check for bullet points or numbered items
                structure_score = 0.5 if re.search(
                    r'[-•]\d+\.]\s+\w+', content) else 0.0

                # Check for legal references and terms
                legal_score = 0.5 if any(term in content.lower()
                                         for term in self.legal_terms_patterns) else 0.0

                section_scores.append(
                    (length_score + structure_score + legal_score) / 3)
            else:
                section_scores.append(0.0)

        # Weight sections differently based on complexity
        if complexity.lower() == "high":
            weights = [0.2, 0.3, 0.3, 0.2]  # More weight on analysis
        elif complexity.lower() == "low":
            # More weight on scope and conclusion
            weights = [0.3, 0.2, 0.2, 0.3]
        else:
            weights = [0.25, 0.25, 0.25, 0.25]  # Equal weights

        return sum(score * weight for score, weight in zip(section_scores, weights))

    def add_result(
        self,
        prompt_name: str,
        question: str,
        answer: str,
        metrics: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an evaluation result.

        Args:
            prompt_name: Name of the prompt template
            question: Original question
            answer: Generated answer
            metrics: Evaluation metrics
            metadata: Additional metadata
        """
        result = EvaluationResult(
            prompt_name=prompt_name,
            question=question,
            answer=answer,
            metrics=metrics,
            metadata=metadata or {}
        )
        self.results.append(result)

    def save_results(self, filename: Optional[str] = None) -> None:
        """Save evaluation results to a JSON file.

        Args:
            filename: Optional filename, defaults to timestamp
        """
        if filename is None:
            filename = f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        path = os.path.join(self.output_dir, filename)

        # Convert results to dictionary format
        results_dict = [
            {
                "prompt_name": r.prompt_name,
                "question": r.question,
                "answer": r.answer,
                "metrics": r.metrics,
                "metadata": r.metadata,
                "timestamp": r.timestamp
            }
            for r in self.results
        ]

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, ensure_ascii=False, indent=2)

    def load_results(self, filename: str) -> None:
        """Load evaluation results from a JSON file.

        Args:
            filename: Name of the file to load
        """
        path = os.path.join(self.output_dir, filename)

        with open(path, 'r', encoding='utf-8') as f:
            results_dict = json.load(f)

        self.results = [
            EvaluationResult(**result)
            for result in results_dict
        ]

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of evaluation results.

        Returns:
            Dict[str, Any]: Summary statistics
        """
        if not self.results:
            return {"error": "No results available"}

        summary = {
            "total_evaluations": len(self.results),
            "prompts_evaluated": len(set(r.prompt_name for r in self.results)),
            "average_scores": {},
            "best_performing_prompt": "",
            "timestamp": datetime.now().isoformat()
        }

        # Calculate average scores per prompt
        prompt_scores: Dict[str, List[float]] = {}
        for result in self.results:
            if result.prompt_name not in prompt_scores:
                prompt_scores[result.prompt_name] = []
            prompt_scores[result.prompt_name].append(
                result.metrics["overall_score"])

        # Calculate averages and find best prompt
        best_score = 0
        for prompt_name, scores in prompt_scores.items():
            avg_score = sum(scores) / len(scores)
            summary["average_scores"][prompt_name] = avg_score
            if avg_score > best_score:
                best_score = avg_score
                summary["best_performing_prompt"] = prompt_name

        return summary

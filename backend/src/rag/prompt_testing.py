"""Script for testing and evaluating different prompt templates."""
import os
from typing import Dict, List

from langchain_openai import ChatOpenAI

from .prompts import (
    BasicLegalPrompt,
    MultiStepLegalPrompt,
    PromptEvaluator,
    StructuredLegalPrompt,
)
from .rag_system import TurkishLegalRAG

# Get the absolute path to the data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


def get_test_questions() -> List[Dict[str, str]]:
    """Get a list of test questions with expected structures."""
    return [
        {
            "question": "Ceza sorumluluğunun esasları nelerdir?",
            "expected_structure": [
                "SORU KAPSAMI",
                "İLGİLİ KANUN MADDELERİ",
                "HUKUKİ ANALİZ",
                "SONUÇ",
            ],
            "metadata": {
                "complexity": "high",
                "expected_terms": ["kusur", "isnat yeteneği", "kast", "taksir"],
                "min_articles": 3,
            },
        },
        {
            "question": "Türk Ceza Kanunu'nda taksir nasıl düzenlenmiştir?",
            "expected_structure": [
                "SORU KAPSAMI",
                "İLGİLİ KANUN MADDELERİ",
                "HUKUKİ ANALİZ",
                "SONUÇ",
            ],
            "metadata": {
                "complexity": "medium",
                "expected_terms": ["taksir", "ihmal", "öngörme"],
                "min_articles": 2,
            },
        },
        {
            "question": "Hukuka uygunluk nedenleri nelerdir?",
            "expected_structure": [
                "SORU KAPSAMI",
                "İLGİLİ KANUN MADDELERİ",
                "HUKUKİ ANALİZ",
                "SONUÇ",
            ],
            "metadata": {
                "complexity": "high",
                "expected_terms": [
                    "meşru müdafaa",
                    "zorunluluk hali",
                    "hakkın kullanılması",
                    "görevin ifası",
                ],
                "min_articles": 4,
            },
        },
        {
            "question": "Teşebbüs halinde ceza nasıl belirlenir?",
            "expected_structure": [
                "SORU KAPSAMI",
                "İLGİLİ KANUN MADDELERİ",
                "HUKUKİ ANALİZ",
                "SONUÇ",
            ],
            "metadata": {
                "complexity": "medium",
                "expected_terms": ["teşebbüs", "hazırlık hareketi", "icra hareketi"],
                "min_articles": 2,
            },
        },
        {
            "question": "İştirak halinde işlenen suçlarda sorumluluk nasıl belirlenir?",
            "expected_structure": [
                "SORU KAPSAMI",
                "İLGİLİ KANUN MADDELERİ",
                "HUKUKİ ANALİZ",
                "SONUÇ",
            ],
            "metadata": {
                "complexity": "high",
                "expected_terms": ["iştirak", "fail", "azmettirme", "yardım etme"],
                "min_articles": 3,
            },
        },
    ]


def test_prompts(
    rag_system: TurkishLegalRAG, llm: ChatOpenAI, evaluator: PromptEvaluator
) -> None:
    """Test different prompt templates and evaluate their performance."""
    # Initialize prompt templates
    prompts = {
        "basic": BasicLegalPrompt(),
        "structured": StructuredLegalPrompt(),
        "multi_step": MultiStepLegalPrompt(),
    }

    # Get test questions
    test_questions = get_test_questions()

    # Test each prompt template
    for prompt_name, prompt in prompts.items():
        print(f"\nTesting {prompt_name} prompt template...")

        for test_case in test_questions:
            question = test_case["question"]
            expected_structure = test_case["expected_structure"]
            metadata = test_case.get("metadata", {})

            print(f"\nProcessing question: {question}")
            print(f"Complexity: {metadata.get('complexity', 'medium')}")
            print(f"Expected terms: {metadata.get('expected_terms', [])}")

            # Get relevant documents
            context = rag_system.retrieve(question)
            formatted_context = rag_system.format_context(context)

            try:
                # Format prompt and get response
                formatted_prompt = prompt.format(
                    context=formatted_context, question=question
                )
                response = llm.invoke(formatted_prompt)
                answer = (
                    response.content if hasattr(response, "content") else str(response)
                )

                # Evaluate response
                metrics = evaluator.evaluate_response(
                    prompt_name=prompt_name,
                    question=question,
                    answer=answer,
                    expected_structure=expected_structure,
                    metadata=metadata,
                )

                # Add result
                evaluator.add_result(
                    prompt_name=prompt_name,
                    question=question,
                    answer=answer,
                    metrics=metrics,
                    metadata={
                        "template_type": prompt_name,
                        "expected_structure": expected_structure,
                        "complexity": metadata.get("complexity", "medium"),
                        "expected_terms": metadata.get("expected_terms", []),
                    },
                )

                print("\nMetrics:")
                for metric, value in metrics.items():
                    print(f"- {metric}: {value:.3f}")

            except Exception as e:
                print(
                    f"Error testing prompt {prompt_name} with question '{question}': {str(e)}"
                )

    # Save results
    evaluator.save_results()

    # Print summary
    summary = evaluator.get_summary()
    print("\nEvaluation Summary:")
    print(f"Total evaluations: {summary['total_evaluations']}")
    print(f"Prompts evaluated: {summary['prompts_evaluated']}")
    print("\nAverage scores per prompt:")
    for prompt_name, score in summary["average_scores"].items():
        print(f"{prompt_name}: {score:.3f}")
    print(f"\nBest performing prompt: {summary['best_performing_prompt']}")

    # Print detailed analysis
    print("\nDetailed Analysis:")
    for prompt_name in prompts:
        prompt_results = [r for r in evaluator.results if r.prompt_name == prompt_name]
        print(f"\n{prompt_name.upper()} PROMPT:")

        # Analyze performance by complexity
        for complexity in ["low", "medium", "high"]:
            complexity_results = [
                r for r in prompt_results if r.metadata.get("complexity") == complexity
            ]
            if complexity_results:
                avg_score = sum(
                    r.metrics["overall_score"] for r in complexity_results
                ) / len(complexity_results)
                print(f"- {complexity.title()} complexity questions: {avg_score:.3f}")

        # Analyze term usage
        term_scores = [r.metrics["term_usage_score"] for r in prompt_results]
        avg_term_score = sum(term_scores) / len(term_scores) if term_scores else 0
        print(f"- Average term usage score: {avg_term_score:.3f}")

        # Analyze structure adherence
        structure_scores = [r.metrics["structure_score"] for r in prompt_results]
        avg_structure_score = (
            sum(structure_scores) / len(structure_scores) if structure_scores else 0
        )
        print(f"- Average structure score: {avg_structure_score:.3f}")


if __name__ == "__main__":
    # Initialize components
    rag_system = TurkishLegalRAG(
        law_json_path=os.path.join(
            DATA_DIR, "processed", "criminal_law", "processed_law.json"
        ),
        terms_json_path=os.path.join(
            DATA_DIR, "processed", "legal_terms", "legal_terms.json"
        ),
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    evaluator = PromptEvaluator(output_dir="evaluation_results")

    # Run tests
    test_prompts(rag_system, llm, evaluator)

"""Example usage of the Turkish Legal RAG system. This module demonstrates basic usage patterns and common operations."""

import logging

from src.rag import LegalQAChain, TurkishLegalRAG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the example usage demonstration.

    This function demonstrates:
    - Setting up the RAG system
    - Creating a QA chain
    - Processing a sample question
    - Retrieving and displaying results
    """
    try:
        # Initialize RAG system
        rag_system = TurkishLegalRAG(
            law_json_path="data/processed/processed_law.json",
            terms_json_path="data/processed/legal_terms/legal_terms.json",
        )

        # Create QA chain
        qa_chain = LegalQAChain(rag_system)

        # Example question
        question = "TCK'da taksir nedir ve nasıl düzenlenmiştir?"
        logger.info(f"Processing question: {question}")

        # Get answer
        answer = qa_chain.run(question=question)
        logger.info(f"Answer: {answer}")

        # Get relevant sources
        sources = rag_system.retrieve(query=question, n_results=3)
        logger.info("Relevant sources:")
        for source in sources:
            logger.info(f"- {source['content'][:200]}...")

    except Exception as e:
        logger.error(f"Error in example: {str(e)}")
        raise


if __name__ == "__main__":
    main()

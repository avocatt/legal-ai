"""
Basic usage example of the Turkish Legal QA system.
This script demonstrates the core functionality of the system.
"""

import os
from dotenv import load_dotenv
from legal_ai.rag import TurkishLegalRAG, LegalQAChain
from langchain_openai import ChatOpenAI


def main():
    # Load environment variables
    load_dotenv()

    # Initialize the RAG system
    rag_system = TurkishLegalRAG("data/processed/processed_law.json")

    # Initialize LLM
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0
    )

    # Create QA chain
    qa_chain = LegalQAChain(rag_system, llm)

    # Example questions
    questions = [
        "Ceza kanununun temel amacı nedir?",
        "Türk Ceza Kanunu hangi durumlarda yabancı ülkelerde işlenen suçlara uygulanır?",
        "Ceza sorumluluğunun esasları nelerdir?"
    ]

    # Process each question
    for question in questions:
        print(f"\nQ: {question}")
        try:
            answer = qa_chain.run(question)
            print(f"\nA: {answer}")
        except Exception as e:
            print(f"Error processing question: {str(e)}")
        print("-" * 50)


if __name__ == "__main__":
    main()

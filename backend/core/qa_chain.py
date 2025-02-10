"""Question answering chain implementation for the Turkish Legal RAG system.

This module provides the QA chain that combines the RAG system with a language model
to generate accurate answers to legal questions.
"""

from typing import Dict, Optional

from langchain_core.language_models.base import BaseLanguageModel

from .prompts import StructuredLegalPrompt
from .rag_system import TurkishLegalRAG


class LegalQAChain:
    """Chain for answering legal questions using RAG and LLM.

    This class combines the Turkish Legal RAG system with a language model to
    generate accurate and well-structured answers to legal questions. It uses
    a structured prompt template to ensure consistent and comprehensive responses.

    Attributes:
        rag_system: Turkish Legal RAG system for retrieving relevant documents
        llm: Language model for generating answers
        prompt_template: Template for structuring the prompts
    """

    def __init__(
        self,
        rag_system: TurkishLegalRAG,
        llm: Optional[BaseLanguageModel] = None,
    ):
        """Initialize the QA chain.

        Args:
            rag_system: Turkish Legal RAG system instance
            llm: Optional language model (if not provided, will use default)
        """
        self.rag_system = rag_system
        self.llm = llm
        self.prompt_template = StructuredLegalPrompt()

    def run(
        self,
        question: str,
        metadata_filter: Optional[Dict[str, str]] = None,
        n_results: int = 5,
    ) -> str:
        """Run the QA chain to get an answer.

        Args:
            question: The legal question to answer
            metadata_filter: Optional filters for document retrieval
            n_results: Number of documents to retrieve (default: 5)

        Returns:
            str: Generated answer to the question

        Raises:
            ValueError: If the question is empty or invalid
            Exception: If there's an error during processing
        """
        if not question or not isinstance(question, str):
            raise ValueError("Question must be a non-empty string")

        try:
            # Retrieve relevant documents
            docs = self.rag_system.retrieve(
                query=question,
                n_results=n_results,
                metadata_filter=metadata_filter,
            )

            # Format context from retrieved documents
            context = self.rag_system.format_context(docs)

            # Format prompt
            prompt = self.prompt_template.format(
                context=context,
                question=question,
            )

            # Generate answer using LLM
            if self.llm:
                response = self.llm.invoke(prompt)
                return response.content

            return "No language model provided. Please initialize with a valid LLM."

        except Exception as e:
            raise Exception(f"Error in QA chain: {str(e)}")

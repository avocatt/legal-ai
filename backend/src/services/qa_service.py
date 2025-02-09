"""Question answering service implementation.

This module provides the service layer for handling legal question answering,
integrating the RAG system with the FastAPI application.
"""

import time
from typing import Dict, Optional

from langchain_openai import ChatOpenAI
from src.rag import LegalQAChain, TurkishLegalRAG

from ..core.config import get_settings


class QAService:
    """Service class for handling legal question answering using RAG system.

    This service integrates a Turkish Legal RAG system with LangChain's ChatOpenAI
    to provide accurate answers to legal questions. It uses a combination of
    law documents and legal terminology for comprehensive responses.

    Attributes:
        settings: Application configuration settings
        rag_system: Turkish Legal RAG system instance
        llm: LangChain ChatOpenAI model instance
        qa_chain: Legal QA chain combining RAG and LLM
    """

    def __init__(self):
        """Initialize the QA service with necessary components.

        Sets up the RAG system with law and terminology data, configures the
        language model, and creates the QA chain.
        """
        self.settings = get_settings()
        self.rag_system = TurkishLegalRAG(
            law_json_path="data/processed/criminal_law/processed_law.json",
            terms_json_path="data/processed/legal_terms/legal_terms.json",
            collection_name=self.settings.COLLECTION_NAME,
            embedding_model=self.settings.EMBEDDING_MODEL,
        )

        self.llm = ChatOpenAI(model_name=self.settings.LLM_MODEL, temperature=0)

        self.qa_chain = LegalQAChain(self.rag_system, self.llm)

    async def get_answer(
        self,
        question: str,
        metadata_filter: Optional[Dict[str, str]] = None,
        n_results: int = 5,
    ) -> Dict:
        """Process a legal question and return an answer with relevant sources.

        Args:
            question: The legal question to be answered
            metadata_filter: Optional filters to apply when retrieving sources
            n_results: Number of source documents to retrieve (default: 5)

        Returns:
            Dict containing:
                - answer: Generated response to the question
                - confidence_score: Confidence level of the answer
                - sources: Retrieved relevant source documents
                - processing_time: Time taken to process the question

        Raises:
            Exception: If there's an error processing the question
        """
        start_time = time.time()

        try:
            # Get answer from QA chain
            answer = self.qa_chain.run(
                question=question, metadata_filter=metadata_filter
            )

            # Get sources (including both articles and terms)
            sources = self.rag_system.retrieve(
                query=question, n_results=n_results, metadata_filter=metadata_filter
            )

            # Calculate processing time
            processing_time = time.time() - start_time

            return {
                "answer": answer,
                "confidence_score": 0.8,  # TODO: Implement confidence scoring
                "sources": sources,
                "processing_time": processing_time,
            }

        except Exception as e:
            raise Exception(f"Error processing question: {str(e)}")


# Create singleton instance
qa_service = QAService()

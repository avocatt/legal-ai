"""Question answering chain implementation for the Turkish Legal RAG system.

This module provides the QA chain that combines the RAG system with a language model
to generate accurate answers to legal questions.
"""

from typing import Dict, List, Optional

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from .prompts import StructuredLegalPrompt


class QAChain:
    """Chain for question answering using the Turkish Legal RAG system."""

    def __init__(self):
        """Initialize the QA chain."""
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
        )
        self.prompt = StructuredLegalPrompt()
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    async def generate_answer(
        self,
        question: str,
        documents: List[Dict],
        legal_terms: Optional[List[Dict]] = None,
    ) -> str:
        """Generate an answer using the QA chain.

        Args:
            question: The question to answer
            documents: Retrieved documents to use as context
            legal_terms: Optional relevant legal terms

        Returns:
            The generated answer
        """
        # Format context from documents
        context = "\n\n".join(
            f"Article {doc['metadata']['number']}: {doc['content']}"
            for doc in documents
        )

        # Format legal terms if provided
        terms_context = ""
        if legal_terms:
            terms_context = "\n".join(
                f"{term['term']}: {term['definition']}"
                for term in legal_terms
            )

        # Generate answer
        result = await self.chain.ainvoke({
            "question": question,
            "context": context,
            "legal_terms": terms_context,
        })

        return result["text"]

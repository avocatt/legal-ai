"""
QA chain implementation for the Turkish Legal RAG system.
"""

from typing import Any, Dict, List, Optional

from langchain.chains import LLMChain
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate

from .retriever import DocumentRetriever


class LegalQAChain:
    """A chain that combines RAG retrieval with LLM for legal QA."""

    def __init__(self,
                 retriever: DocumentRetriever,
                 llm: Any,
                 callbacks: Optional[List[BaseCallbackHandler]] = None):
        """Initialize the QA chain with a retriever and LLM."""
        if not isinstance(retriever, DocumentRetriever):
            raise TypeError("retriever must be an instance of DocumentRetriever")

        self.retriever = retriever
        self.llm = llm
        self.callbacks = callbacks

        # Default prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal expert assistant specializing in Turkish Criminal Law. 
            Your task is to answer questions about the law using the provided context.
            Always cite the specific articles you reference in your answer.
            If the provided context doesn't contain enough information to answer the question confidently,
            say so explicitly."""),
            ("human", "Context:\n{context}\n\nQuestion: {question}\n\nPlease provide a detailed answer based on the Turkish Criminal Law:"),
        ])

        self.chain = LLMChain(llm=llm, prompt=self.prompt, callbacks=callbacks)

    def set_custom_prompt(self, prompt: ChatPromptTemplate):
        """Set a custom prompt template for the chain."""
        self.prompt = prompt
        self.chain = LLMChain(llm=self.llm, prompt=prompt, callbacks=self.callbacks)

    def run(self,
            question: str,
            n_results: int = 5,
            metadata_filter: Optional[Dict[str, str]] = None) -> str:
        """Run the full RAG chain to answer a question."""
        if not question or not isinstance(question, str):
            raise ValueError("Question must be a non-empty string")

        try:
            # Retrieve relevant documents
            retrieved_docs = self.retriever.retrieve(question, n_results, metadata_filter)
            if not retrieved_docs:
                return "I couldn't find any relevant information to answer your question."

            # Format context
            context = self.retriever.format_context(retrieved_docs)

            # Generate answer
            response = self.chain.run(context=context, question=question)
            return response
        except Exception as e:
            return f"An error occurred while processing your question: {str(e)}"

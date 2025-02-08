"""Chain for question answering over Turkish legal documents."""

from typing import Dict, Optional

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate

from .rag_system import TurkishLegalRAG


class LegalQAChain:
    """Chain for question answering over Turkish legal documents using a RAG system."""

    def __init__(self, rag_system: TurkishLegalRAG, llm: BaseLanguageModel):
        """Initialize the QA chain.

        Args:
            rag_system: The RAG system to use for document retrieval
            llm: The language model to use for question answering
        """
        self.rag_system = rag_system
        self.llm = llm

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a Turkish legal expert assistant. Use the following "
                    "context to answer the question. If you cannot find the answer "
                    "in the context, say so. Do not make up information.\n\n"
                    "Context:\n{context}\n\n",
                ),
                ("human", "{question}"),
            ]
        )

    def run(
        self,
        question: str,
        metadata_filter: Optional[Dict[str, str]] = None,
        include_blog: bool = True,
    ) -> str:
        """Run the QA chain on a question.

        Args:
            question: The question to answer
            metadata_filter: Optional metadata filters for document retrieval
            include_blog: Whether to include blog articles in retrieval

        Returns:
            str: The answer to the question
        """
        # Retrieve relevant documents
        docs = self.rag_system.retrieve(
            query=question,
            metadata_filter=metadata_filter,
            include_blog=include_blog,
        )

        # Format the context
        context = self.rag_system.format_context(docs)

        # Generate the answer
        chain = self.prompt | self.llm
        response = chain.invoke({"context": context, "question": question})

        return response.content

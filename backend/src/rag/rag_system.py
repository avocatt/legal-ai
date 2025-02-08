"""Turkish Legal RAG system implementation.

This module provides the core RAG system for Turkish legal question answering,
integrating document retrieval, legal terminology, and context management.
"""

import json
from typing import Any, Dict, List, Optional

from .legal_terms import LegalTerminology
from .retriever import DocumentRetriever


class TurkishLegalRAG:
    """Turkish Legal RAG system for retrieving and managing legal content.

    This class provides a comprehensive RAG system specifically designed for
    Turkish legal content. It combines document retrieval with legal terminology
    management to provide accurate and relevant context for question answering.

    Attributes:
        retriever: Document retriever for law articles and blog content
        terminology: Legal terminology manager for term definitions
    """

    def __init__(
        self,
        law_json_path: str,
        terms_json_path: str,
        collection_name: str = "turkish_criminal_law",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the Turkish Legal RAG system.

        Args:
            law_json_path: Path to the law articles JSON file
            terms_json_path: Path to the legal terms JSON file
            collection_name: Name for the vector store collection
            embedding_model: Name of the embedding model to use
        """
        self.retriever = DocumentRetriever(
            law_json_path=law_json_path,
            collection_name=collection_name,
            embedding_model=embedding_model,
        )
        self.terminology = LegalTerminology(
            terms_json_path=terms_json_path,
            embedding_model=embedding_model,
        )

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        metadata_filter: Optional[Dict[str, str]] = None,
    ) -> List[Dict]:
        """Retrieve relevant documents and legal terms for a query.

        Args:
            query: The search query
            n_results: Number of results to retrieve (default: 5)
            metadata_filter: Optional filters for document retrieval

        Returns:
            List[Dict]: Combined list of relevant documents and terms

        Raises:
            ValueError: If the query is empty or invalid
            Exception: If there's an error during retrieval
        """
        # Get relevant documents
        docs = self.retriever.retrieve(
            query=query,
            n_results=n_results,
            metadata_filter=metadata_filter,
        )

        # Get relevant legal terms
        terms = self.terminology.get_relevant_terms(query, n_results=3)

        # Combine and format results
        results = []
        for doc in docs:
            results.append(
                {
                    "id": doc["id"],
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "distance": doc["distance"],
                }
            )

        for term in terms:
            results.append(
                {
                    "id": f"term_{term['term']}",
                    "content": f"{term['term']}: {term['definition']}",
                    "metadata": {"type": "legal_term"},
                    "distance": term["distance"],
                }
            )

        return sorted(
            results, key=lambda x: x["distance"] if x["distance"] else float("inf")
        )

    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into a context string.

        Args:
            retrieved_docs: List of retrieved documents and terms

        Returns:
            str: Formatted context string for the language model

        Raises:
            ValueError: If retrieved_docs is empty or invalid
        """
        if not retrieved_docs:
            return ""

        context_parts = []

        # Group documents by type
        articles = []
        terms = []

        for doc in retrieved_docs:
            if doc["metadata"].get("type") == "legal_term":
                terms.append(doc["content"])
            else:
                articles.append(doc["content"])

        # Format articles
        if articles:
            context_parts.append("İlgili Kanun Maddeleri:")
            context_parts.extend(articles)

        # Format terms
        if terms:
            context_parts.append("\nİlgili Hukuki Terimler:")
            context_parts.extend(terms)

        return "\n\n".join(context_parts)

    def _load_law_data(self, json_path: str) -> Dict[str, Any]:
        """Load law data from JSON file.

        Args:
            json_path: Path to the JSON file

        Returns:
            Dict containing the law data
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading law data: {str(e)}")

    def _initialize_law_collection(self):
        """Initialize the law collection with articles."""
        documents = []
        ids = []
        metadatas = []

        for article in self.law_data["articles"]:
            article_id = f"article_{len(ids)}"
            ids.append(article_id)
            documents.append(article["content"])
            metadatas.append(
                {
                    "number": article["number"],
                    "book": article.get("book"),
                    "part": article.get("part"),
                    "chapter": article.get("chapter"),
                    "type": "article",
                }
            )

        # Add documents in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            self.law_collection.add(
                documents=documents[i:end_idx],
                ids=ids[i:end_idx],
                metadatas=metadatas[i:end_idx],
            )

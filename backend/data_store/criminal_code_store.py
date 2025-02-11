"""Criminal Code Vectorizer.

This module handles the vectorization and retrieval of Turkish Criminal Code articles.
"""

import json
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.errors import InvalidCollectionException

from api import get_settings
from utils.helpers import load_json_file
from .embeddings import get_embeddings_model


class CriminalCodeVectorizer:
    """Vectorizer for Turkish Criminal Code articles."""

    def __init__(
        self,
        law_json_path: str = None,
        collection_name: str = "turkish_criminal_law",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the Criminal Code vectorizer."""
        self.settings = get_settings()
        self.law_data = self._load_law_data(
            law_json_path or self.settings.CRIMINAL_CODE_PATH)
        self.embeddings = get_embeddings_model(embedding_model)

        # Initialize Chroma client with persistent storage
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.settings.CHROMA_DB_DIR))
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name, embedding_function=self.embeddings
            )
            print(f"Using existing collection: {collection_name}")
        except (ValueError, InvalidCollectionException):
            print(f"Creating new collection: {collection_name}")
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embeddings,
                metadata={"description": "Turkish Legal Text Embeddings"},
            )
            self._initialize_vector_store()

    def _load_law_data(self, json_path: str) -> Dict[str, Any]:
        """Load law data from JSON file."""
        try:
            return load_json_file(json_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Law data file not found: {json_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in law data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading law data: {str(e)}")

    def _initialize_vector_store(self):
        """Initialize the vector store with articles."""
        documents = []
        ids = []
        metadatas = []

        for book in self.law_data["books"]:
            for part in book["parts"]:
                for chapter in part["chapters"]:
                    for article in chapter["articles"]:
                        # Create a document for the full article
                        article_text = (
                            f"Article {article['number']}: {article['content']}"
                        )
                        article_id = f"article_{article['number']}"

                        documents.append(article_text)
                        ids.append(article_id)
                        metadatas.append(
                            {
                                "type": "article",
                                "number": article["number"],
                                "book": book["title"],
                                "part": part["title"],
                                "chapter": chapter["title"],
                            }
                        )

        # Add documents to the collection
        if documents:
            self.collection.add(documents=documents,
                                ids=ids, metadatas=metadatas)

    def retrieve(
        self,
        query: str,
        metadata_filter: Optional[Dict[str, str]] = None,
        n_results: int = 5,
    ) -> List[Dict]:
        """Retrieve relevant criminal code articles.

        Args:
            query: The search query
            metadata_filter: Optional filters for specific sections
            n_results: Number of results to retrieve

        Returns:
            List of relevant articles with metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=metadata_filter,
        )

        return [
            {
                "id": result["id"],
                "content": result["content"],
                "metadata": result["metadata"],
                "distance": result["distance"],
            }
            for result in results
        ]

    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into a context string."""
        context_parts = []
        for doc in retrieved_docs:
            if doc["metadata"]["type"] == "article":
                context_parts.append(
                    f"Article {doc['metadata']['number']}: {doc['content']}"
                )
            else:
                context_parts.append(
                    f"From Article {doc['metadata']['article_number']}: {doc['content']}"
                )
        return "\n\n".join(context_parts)

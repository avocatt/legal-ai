"""Turkish Legal RAG retriever implementation."""

import json
import os
from typing import Any, Dict, List, Optional

import chromadb

from .embeddings import get_embedding_function


class DocumentRetriever:
    """Handles document retrieval and vector store management."""

    def __init__(
        self,
        law_json_path: str,
        collection_name: str = "turkish_criminal_law",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the retriever with law data and embedding model."""
        self.law_data = self._load_law_data(law_json_path)

        # Get embedding function
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        self.embedding_function = get_embedding_function(embedding_model, hf_token)

        # Initialize Chroma client and collection
        self.chroma_client = chromadb.Client()
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name, embedding_function=self.embedding_function
            )
            print(f"Using existing collection: {collection_name}")
        except (ValueError, chromadb.errors.InvalidCollectionException):
            print(f"Creating new collection: {collection_name}")
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Turkish Legal Text Embeddings"},
            )
            self._initialize_vector_store()

    def _load_law_data(self, json_path: str) -> Dict[str, Any]:
        """Load the processed law data from JSON."""
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Law data file not found: {json_path}")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid law data format")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in law data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading law data: {str(e)}")

    def _initialize_vector_store(self):
        """Initialize the vector store with articles and provisions."""
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

                        # Create documents for key provisions
                        if "key_provisions" in article:
                            for idx, provision in enumerate(article["key_provisions"]):
                                provision_id = f"provision_{article['number']}_{idx}"
                                documents.append(provision)
                                ids.append(provision_id)
                                metadatas.append(
                                    {
                                        "type": "provision",
                                        "article_number": article["number"],
                                        "provision_index": idx,
                                        "book": book["title"],
                                        "part": part["title"],
                                        "chapter": chapter["title"],
                                    }
                                )

        # Add documents to the collection
        self.collection.add(documents=documents, ids=ids, metadatas=metadatas)

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        metadata_filter: Optional[Dict[str, str]] = None,
    ) -> List[Dict]:
        """Retrieve relevant documents for a query with optional metadata filtering."""
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        if n_results < 1:
            raise ValueError("n_results must be a positive integer")

        query_params = {"query_texts": [query], "n_results": n_results}

        if metadata_filter:
            if not isinstance(metadata_filter, dict):
                raise ValueError("metadata_filter must be a dictionary")
            query_params["where"] = metadata_filter

        try:
            results = self.collection.query(**query_params)
            return self._format_search_results(results)
        except Exception as e:
            print(f"Error during retrieval: {str(e)}")
            return []

    def _format_search_results(self, results: Dict) -> List[Dict]:
        """Format search results into a more usable structure."""
        formatted_results = []
        if not results["ids"]:
            return formatted_results

        for idx, doc_id in enumerate(results["ids"][0]):
            formatted_results.append(
                {
                    "id": doc_id,
                    "content": results["documents"][0][idx],
                    "metadata": results["metadatas"][0][idx],
                    "distance": results.get("distances", [[]])[0][idx]
                    if "distances" in results
                    else None,
                }
            )
        return formatted_results

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

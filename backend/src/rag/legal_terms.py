"""Legal terminology management and integration with the Turkish Legal RAG system."""

import json
import os
from typing import Dict, List, Optional

import chromadb
from chromadb.errors import InvalidCollectionException
from chromadb.utils import embedding_functions

# Create persistent storage directory if it doesn't exist
CHROMA_DB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db"
)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)


class LegalTerminology:
    """Manages legal terminology vector database and integration with RAG system."""

    def __init__(
        self,
        terms_json_path: str,
        collection_name: str = "turkish_legal_terms",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        hf_token: Optional[str] = None,
    ):
        """Initialize the legal terminology system."""
        self.terms_data = self._load_terms(terms_json_path)

        # Initialize embedding function
        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model, token=hf_token
            )
        )

        # Initialize Chroma client with persistent storage
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name, embedding_function=self.embedding_function
            )
            print(f"Using existing legal terms collection: {collection_name}")
        except (ValueError, InvalidCollectionException):
            print(f"Creating new legal terms collection: {collection_name}")
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Turkish Legal Terms Embeddings"},
            )
            self._initialize_vector_store()

    def _load_terms(self, json_path: str) -> Dict[str, str]:
        """Load legal terms from JSON file."""
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _initialize_vector_store(self):
        """Initialize the vector store with legal terms and their definitions."""
        documents = []
        ids = []
        metadatas = []

        for term, definition in self.terms_data.items():
            # Create a structured document combining term and definition
            document = f"[TERM] {term}\n[DEFINITION] {definition}"
            term_id = f"term_{len(ids)}"

            documents.append(document)
            ids.append(term_id)
            metadatas.append({"term": term, "type": "legal_term"})

        # Add documents to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            self.collection.add(
                documents=documents[i:end_idx],
                ids=ids[i:end_idx],
                metadatas=metadatas[i:end_idx],
            )

    def get_relevant_terms(self, context: str, n_results: int = 5) -> List[Dict]:
        """
        Retrieve relevant legal terms based on the given context.

        Args:
            context: The text to find relevant terms for (can be a question or article text)
            n_results: Number of relevant terms to retrieve

        Returns:
            List of dictionaries containing term information
        """
        results = self.collection.query(query_texts=[context], n_results=n_results)

        terms = []
        for idx, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][idx]
            terms.append(
                {
                    "term": metadata["term"],
                    "definition": doc.split("[DEFINITION]")[1].strip(),
                    "distance": results["distances"][0][idx]
                    if "distances" in results
                    else None,
                }
            )

        return terms

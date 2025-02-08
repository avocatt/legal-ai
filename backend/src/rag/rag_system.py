"""Turkish Legal RAG system implementation."""

import json
import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.utils import embedding_functions

from .legal_terms import LegalTerminology

# Create persistent storage directory if it doesn't exist
CHROMA_DB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db"
)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)


class TurkishLegalRAG:
    """RAG system for Turkish Criminal Law."""

    def __init__(
        self,
        law_json_path: str,
        terms_json_path: Optional[str] = None,
        law_collection_name: str = "turkish_criminal_law",
        blog_collection_name: str = "turkish_criminal_law_blog",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the RAG system.

        Args:
            law_json_path: Path to the processed law JSON file
            terms_json_path: Path to the legal terms JSON file
            law_collection_name: Name for the law articles collection
            blog_collection_name: Name for the blog articles collection
            embedding_model: Name of the embedding model to use
        """
        self.law_data = self._load_law_data(law_json_path)
        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model
            )
        )

        # Initialize Chroma client with persistent storage
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

        # Initialize law collection
        try:
            self.law_collection = self.chroma_client.get_collection(
                name=law_collection_name, embedding_function=self.embedding_function
            )
        except ValueError:
            self.law_collection = self.chroma_client.create_collection(
                name=law_collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Turkish Criminal Law Articles"},
            )
            self._initialize_law_collection()

        # Initialize legal terminology if path provided
        self.legal_terms = None
        if terms_json_path:
            self.legal_terms = LegalTerminology(
                terms_json_path=terms_json_path, embedding_model=embedding_model
            )

    def _validate_blog_against_law(self, blog_doc: Dict, law_docs: List[Dict]) -> bool:
        """Validate blog content against law articles.

        Args:
            blog_doc: Blog document to validate
            law_docs: List of relevant law articles

        Returns:
            bool: True if blog content is valid, False otherwise
        """
        try:
            # Extract TCK references from blog
            blog_refs = blog_doc["metadata"].get("tck_references", [])
            if not blog_refs:
                return False

            # Check if referenced articles are in law_docs
            law_refs = {doc["metadata"]["number"] for doc in law_docs}
            return any(ref in law_refs for ref in blog_refs)

        except KeyError:
            return False

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        metadata_filter: Optional[Dict[str, str]] = None,
        include_blog: bool = True,
    ) -> List[Dict]:
        """Retrieve relevant documents based on semantic similarity.

        Args:
            query: Search query
            n_results: Number of results to return
            metadata_filter: Optional filters for document retrieval
            include_blog: Whether to include blog articles

        Returns:
            List of relevant documents with metadata
        """
        # Get relevant law articles
        law_results = self.law_collection.query(
            query_texts=[query], n_results=n_results, where=metadata_filter
        )

        # Convert to list of dictionaries
        documents = []
        for idx, doc in enumerate(law_results["documents"][0]):
            metadata = law_results["metadatas"][0][idx]
            distance = (
                law_results["distances"][0][idx] if "distances" in law_results else None
            )
            documents.append(
                {
                    "id": law_results["ids"][0][idx],
                    "content": doc,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        # Get relevant legal terms if available
        if self.legal_terms:
            term_results = self.legal_terms.get_relevant_terms(
                context=query, n_results=2
            )
            for term in term_results:
                documents.append(
                    {
                        "id": f"term_{len(documents)}",
                        "content": f"{term['term']}: {term['definition']}",
                        "metadata": {"type": "legal_term"},
                        "distance": term.get("distance"),
                    }
                )

        return sorted(documents, key=lambda x: x.get("distance", 1))

    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into a context string.

        Args:
            retrieved_docs: List of retrieved documents

        Returns:
            str: Formatted context string
        """
        context_parts = []

        # Process law articles
        law_articles = [
            doc for doc in retrieved_docs if doc["metadata"].get("type") != "legal_term"
        ]
        if law_articles:
            context_parts.append("TCK Maddeleri:")
            for doc in law_articles:
                article_num = doc["metadata"].get("number", "?")
                context_parts.append(f"Madde {article_num}: {doc['content']}")

        # Process legal terms
        legal_terms = [
            doc for doc in retrieved_docs if doc["metadata"].get("type") == "legal_term"
        ]
        if legal_terms:
            context_parts.append("\nHukuki Terimler:")
            for doc in legal_terms:
                context_parts.append(doc["content"])

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

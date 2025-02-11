"""Legal Terms Vectorizer.

This module handles the vectorization and retrieval of Turkish legal terminology.
"""

import json
import numpy as np
from typing import Dict, List

from api.config import get_settings
from .embeddings import get_embeddings_model
from utils.helpers import load_json_file


class LegalTermsVectorizer:
    """Vectorizer for Turkish legal terminology."""

    def __init__(
        self,
        terms_json_path: str = None,
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the Legal Terms vectorizer.

        Args:
            terms_json_path: Path to the legal terms JSON file
            embedding_model: Name of the embedding model to use
        """
        self.settings = get_settings()
        self.terms_data = self._load_terms(
            terms_json_path or self.settings.LEGAL_TERMS_PATH)
        self.embeddings = get_embeddings_model(embedding_model)
        self._initialize_embeddings()

    def get_relevant_terms(
        self,
        query: str,
        n_results: int = 3,
    ) -> List[Dict]:
        """Get relevant legal terms for a query.

        Args:
            query: The search query
            n_results: Number of terms to retrieve

        Returns:
            List of relevant terms with definitions
        """
        query_embedding = self.embeddings([query])[0]

        # Calculate similarities and get top terms
        similarities = []
        for term, data in self.term_embeddings.items():
            similarity = self._calculate_similarity(
                query_embedding, data["embedding"])
            similarities.append((term, similarity, data["definition"]))

        # Sort by similarity and return top n
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [
            {
                "term": term,
                "definition": definition,
                "similarity": float(similarity),
            }
            for term, similarity, definition in similarities[:n_results]
        ]

    def _load_terms(self, json_path: str) -> Dict:
        """Load terms from JSON file."""
        try:
            return load_json_file(json_path)
        except Exception as e:
            raise ValueError(f"Error loading terms: {str(e)}")

    def _initialize_embeddings(self):
        """Initialize embeddings for all terms."""
        self.term_embeddings = {}
        texts = []
        terms = []

        for term_data in self.terms_data:
            term = term_data["term"]
            definition = term_data["definition"]
            texts.append(f"{term}: {definition}")
            terms.append(term)

        # Get embeddings for all texts at once
        embeddings = self.embeddings(texts)

        # Store embeddings with term data
        for term, embedding in zip(terms, embeddings):
            term_data = next(t for t in self.terms_data if t["term"] == term)
            self.term_embeddings[term] = {
                "embedding": embedding,
                "definition": term_data["definition"],
            }

    def _calculate_similarity(self, embedding1, embedding2) -> float:
        """Calculate cosine similarity between two embeddings."""
        return float(np.dot(embedding1, embedding2) /
                     (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

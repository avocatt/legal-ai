"""Legal Terms Vectorizer.

This module handles the vectorization and retrieval of Turkish legal terminology.
"""

import json
from typing import Dict, List

from .embeddings import get_embeddings_model

class LegalTermsVectorizer:
    """Vectorizer for Turkish legal terminology."""
    
    def __init__(
        self,
        terms_json_path: str = "data/legal_terms.json",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the Legal Terms vectorizer.
        
        Args:
            terms_json_path: Path to the legal terms JSON file
            embedding_model: Name of the embedding model to use
        """
        self.terms_data = self._load_terms(terms_json_path)
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
        query_embedding = self.embeddings.encode(query)
        
        # Calculate similarities and get top terms
        similarities = []
        for term, data in self.term_embeddings.items():
            similarity = self._calculate_similarity(query_embedding, data["embedding"])
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
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading terms: {str(e)}")
            
    def _initialize_embeddings(self):
        """Initialize embeddings for all terms."""
        self.term_embeddings = {}
        for term_data in self.terms_data:
            term = term_data["term"]
            definition = term_data["definition"]
            embedding = self.embeddings.encode(term + ": " + definition)
            self.term_embeddings[term] = {
                "embedding": embedding,
                "definition": definition,
            }
            
    def _calculate_similarity(self, embedding1, embedding2) -> float:
        """Calculate cosine similarity between two embeddings."""
        return float(embedding1 @ embedding2.T)

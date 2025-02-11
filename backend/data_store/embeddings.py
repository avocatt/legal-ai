"""Embeddings utilities.

This module provides functions for working with text embeddings using
sentence transformers.
"""

import os
from typing import List, Optional

from chromadb.api.types import EmbeddingFunction
from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddings(EmbeddingFunction):
    """Wrapper for sentence transformer embeddings."""

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"):
        """Initialize the embeddings model.

        Args:
            model_name: Name of the model to use
        """
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts.

        Args:
            input: List of texts to embed

        Returns:
            List of embeddings
        """
        return self.model.encode(input).tolist()


def get_embeddings_model(
    model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    token: Optional[str] = None,
) -> EmbeddingFunction:
    """Get a sentence transformer model for text embeddings.

    Args:
        model_name: Name of the model to use
        token: Optional HuggingFace token for private models

    Returns:
        SentenceTransformer model
    """
    if token:
        os.environ["HUGGINGFACE_TOKEN"] = token

    return SentenceTransformerEmbeddings(model_name)

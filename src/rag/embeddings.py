"""
Embedding functionality for the Turkish Legal RAG system.
"""

import os
from typing import Optional
from chromadb.utils import embedding_functions


def get_embedding_function(
    model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    hf_token: Optional[str] = None
) -> embedding_functions.SentenceTransformerEmbeddingFunction:
    """
    Create an embedding function using the specified model.

    Args:
        model_name: Name of the sentence transformer model to use
        hf_token: Optional Hugging Face token for better performance

    Returns:
        SentenceTransformerEmbeddingFunction: The embedding function
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name,
        token=hf_token
    )

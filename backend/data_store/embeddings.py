"""Embeddings utilities.

This module provides functions for working with text embeddings using
sentence transformers.
"""

import os
from typing import Optional

from sentence_transformers import SentenceTransformer

def get_embeddings_model(
    model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    token: Optional[str] = None,
) -> SentenceTransformer:
    """Get a sentence transformer model for text embeddings.
    
    Args:
        model_name: Name of the model to use
        token: Optional HuggingFace token for private models
        
    Returns:
        SentenceTransformer model
    """
    if token:
        os.environ["HUGGINGFACE_TOKEN"] = token
        
    return SentenceTransformer(model_name)

"""
Helper functions for the Turkish Legal RAG system.
"""

import os
from pathlib import Path
from typing import Optional


def ensure_directory(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory path."""
    data_dir = get_project_root() / 'data'
    ensure_directory(str(data_dir))
    return data_dir


def get_vector_store_path() -> Path:
    """Get the vector store directory path."""
    vector_store_path = get_data_dir() / 'vector_store'
    ensure_directory(str(vector_store_path))
    return vector_store_path


def validate_api_keys() -> None:
    """Validate that necessary API keys are present."""
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Hugging Face token is optional but recommended
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        print("Warning: HUGGINGFACE_TOKEN not found. Some features may be slower.")

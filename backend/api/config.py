"""API configuration settings."""

import os
from pathlib import Path
from typing import List, Union

from pydantic_settings import BaseSettings


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """API settings configuration class."""

    PROJECT_NAME: str = "Turkish Legal AI API"
    API_V1_STR: str = "/api/v1"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Model settings
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    # Data paths - using project root for absolute paths
    DATA_DIR: Path = get_project_root() / "data"
    CRIMINAL_CODE_PATH: Path = DATA_DIR / \
        "processed/criminal_law/turkish_criminal_code/processed_law.json"
    LEGAL_TERMS_PATH: Path = DATA_DIR / \
        "processed/criminal_law/legal_terms/legal_terms.json"
    CHROMA_DB_DIR: Path = DATA_DIR / "chroma_db"

    # API Keys
    OPENAI_API_KEY: str = ""
    HUGGINGFACE_TOKEN: str | None = None

    class Config:
        """Pydantic config class."""
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        """Initialize settings with proper path resolution."""
        super().__init__(**kwargs)
        # Ensure data directories exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Get API settings.

    Returns:
        Settings object with configuration values
    """
    return Settings()

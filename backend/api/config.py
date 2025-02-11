"""API configuration settings."""

from typing import List, Union

from pydantic_settings import BaseSettings


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

    # Data paths
    CRIMINAL_CODE_PATH: str = "../data/processed/criminal_law/turkish_criminal_code/processed_law.json"
    LEGAL_TERMS_PATH: str = "../data/processed/criminal_law/legal_terms/legal_terms.json"
    CHROMA_DB_DIR: str = "../data/chroma_db"

    class Config:
        """Pydantic config class."""
        case_sensitive = True
        env_file = ".env"


def get_settings() -> Settings:
    """Get API settings.

    Returns:
        Settings object with configuration values
    """
    return Settings()

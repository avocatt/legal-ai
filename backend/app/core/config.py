"""Configuration management for the Turkish Legal AI API.

This module handles environment variables and application settings using Pydantic.
"""

from functools import lru_cache
from typing import Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class defines all configuration settings for the application,
    with defaults where appropriate and validation for required values.
    """

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Turkish Legal AI API"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
        "http://localhost:80",
    ]

    # OpenAI Configuration
    OPENAI_API_KEY: str

    # Hugging Face Configuration
    HUGGINGFACE_TOKEN: Optional[str] = None

    # Model Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    LLM_MODEL: str = "gpt-4-turbo-preview"

    # Vector Store Configuration
    COLLECTION_NAME: str = "turkish_criminal_law"

    # RAG Settings
    LAW_JSON_PATH: str = "data/processed/law.json"
    TERMS_JSON_PATH: str = "data/processed/legal_terms.json"

    class Config:
        """Pydantic configuration for settings."""

        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @validator("OPENAI_API_KEY", "HUGGINGFACE_TOKEN")
    def validate_required_env_vars(cls, v: Optional[str], field: str) -> str:
        """Validate that required environment variables are provided.

        Args:
            v (Optional[str]): The value to validate
            field (str): The field name being validated

        Returns:
            str: The validated value

        Raises:
            ValueError: If the required environment variable is not provided
        """
        if not v:
            raise ValueError(f"{field} environment variable must be provided")
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings.

    Returns:
        Settings: Application settings instance
    """
    return Settings()

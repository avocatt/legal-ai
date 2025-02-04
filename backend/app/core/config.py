from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import validator


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Turkish Legal AI"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000",
                                       "http://localhost:8000", "http://localhost", "http://localhost:80"]

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None

    # Hugging Face Configuration
    HUGGINGFACE_TOKEN: Optional[str] = None

    # Model Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"

    # Vector Store Configuration
    COLLECTION_NAME: str = "turkish_criminal_law"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @validator("OPENAI_API_KEY", "HUGGINGFACE_TOKEN")
    def validate_required_env_vars(cls, v: Optional[str]) -> str:
        if not v:
            raise ValueError(f"Environment variable must be provided")
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()

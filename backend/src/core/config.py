"""Configuration management for the application."""

import json
import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, PostgresDsn, field_validator, ValidationInfo, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """Application settings with validation."""
    
    model_config = SettingsConfigDict(
        env_file=".env" if "PYTEST_CURRENT_TEST" not in os.environ else "tests/.env.test",
        case_sensitive=True,
        env_prefix="",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
        json_schema_extra={"format": "uri"},
        validate_default=True,
        str_strip_whitespace=True,
        str_to_lower=False,
    )

    # Core settings
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False
    PROJECT_NAME: str = "Turkish Legal AI API"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        """Assemble database connection URI."""
        if isinstance(v, str):
            return v
        
        data = info.data
        return str(PostgresDsn.build(
            scheme="postgresql",
            username=data.get("POSTGRES_USER"),
            password=data.get("POSTGRES_PASSWORD"),
            host=data.get("POSTGRES_SERVER", "localhost"),
            path=f"/{data.get('POSTGRES_DB', '')}",
        ))

    # Logging
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_FILE: Optional[Path] = None

    @field_validator("LOG_FILE")
    def create_log_directory(cls, v: Optional[Path]) -> Optional[Path]:
        """Create log directory if it doesn't exist."""
        if v:
            v.parent.mkdir(parents=True, exist_ok=True)
        return v

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=[],
        description="List of origins that are allowed to make cross-origin requests",
        validate_default=True,
        json_schema_extra={"format": "uri"},
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse and validate CORS origins from string or list."""
        if isinstance(v, list):
            return [str(origin).strip() for origin in v if str(origin).strip()]
        
        if isinstance(v, str):
            if not v.strip():
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    origins = json.loads(v)
                    if isinstance(origins, list):
                        return [str(origin).strip() for origin in origins if str(origin).strip()]
                except json.JSONDecodeError:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        
        return []

    @field_validator("BACKEND_CORS_ORIGINS")
    def validate_cors_origins(cls, v: List[str]) -> List[AnyHttpUrl]:
        """Validate that each CORS origin is a valid URL."""
        return [AnyHttpUrl(origin) for origin in v]

    # API Keys
    OPENAI_API_KEY: str
    HUGGINGFACE_TOKEN: Optional[str] = None

    # Data paths
    DATA_DIR: Path = Path("data")
    LAW_JSON_PATH: Path = Path("processed/criminal_law/processed_law.json")
    TERMS_JSON_PATH: Path = Path("processed/legal_terms/legal_terms.json")

    @field_validator("LAW_JSON_PATH", "TERMS_JSON_PATH")
    def validate_data_files(cls, v: Path, info: ValidationInfo) -> Path:
        """Validate that data files exist."""
        data = info.data
        data_dir = data.get("DATA_DIR", Path("data"))
        file_path = data_dir / v
        if not file_path.is_file():
            raise ValueError(f"Data file not found: {file_path}")
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def clear_settings_cache() -> None:
    """Clear the settings cache.
    
    This function should be called when environment variables change,
    to ensure the settings are reloaded with the new values.
    """
    get_settings.cache_clear()

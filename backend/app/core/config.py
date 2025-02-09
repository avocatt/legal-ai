"""Configuration management for the Turkish Legal AI API.

This module provides a unified configuration system with validation and documentation.
It handles all application settings including:
- API configuration
- Security settings
- Database configuration
- Model settings
- File paths
- Logging
"""

from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
import json
import logging
import os

from pydantic import (
    AnyHttpUrl,
    EmailStr,
    Field,
    PostgresDsn,
    SecretStr,
    field_validator,
    GetJsonSchemaHandler,
    GetCoreSchemaHandler,
    ValidationInfo,
    BaseModel,
    ValidationError,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource


class Environment(str, Enum):
    """Application environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CorsOrigins:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate_and_parse(value: Any) -> List[str]:
            if isinstance(value, str):
                if value.startswith("["):
                    try:
                        return json.loads(value)
                    except json.JSONDecodeError:
                        pass
                return [i.strip() for i in value.split(",") if i.strip()]
            return value

        return {
            "type": "list",
            "items": {"type": "string"},
            "validator": validate_and_parse,
        }

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: CoreSchema,
        _handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "comma-separated-urls"}


class CustomEnvSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(
        self, field: str, field_info: Any
    ) -> Tuple[Any, str, bool]:
        env_val = os.environ.get(field)
        if env_val is None:
            return None, field, False
        
        # Special handling for CORS origins
        if field == "BACKEND_CORS_ORIGINS":
            if env_val.startswith("["):
                try:
                    return json.loads(env_val), field, False
                except json.JSONDecodeError:
                    pass
            return [i.strip() for i in env_val.split(",") if i.strip()], field, False
        
        return env_val, field, False

    def __call__(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        
        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(field_name, field)
            if field_value is not None:
                data[field_key] = field_value
        
        return data


class Settings(BaseSettings):
    """Application settings with validation and documentation.
    
    This class defines all configuration settings for the application,
    with proper validation, type hints, and documentation for each setting.
    """

    # Environment
    ENVIRONMENT: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Application environment"
    )
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode"
    )

    # API Configuration
    PROJECT_NAME: str = Field(
        default="Turkish Legal AI API",
        description="Name of the project"
    )
    API_V1_STR: str = Field(
        default="/api/v1",
        description="API version 1 prefix"
    )
    SERVER_HOST: AnyHttpUrl = Field(
        default="http://localhost",
        description="Server host URL"
    )
    SERVER_PORT: int = Field(
        default=8000,
        description="Server port"
    )

    # Security
    SECRET_KEY: SecretStr = Field(
        ...,
        description="Secret key for JWT token generation"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT token algorithm"
    )

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=["http://localhost:3000", "http://localhost:8000", "http://localhost"],
        description="List of origins that can access the API"
    )

    # Database
    POSTGRES_SERVER: str = Field(
        default="localhost",
        description="PostgreSQL server hostname"
    )
    POSTGRES_USER: str = Field(
        ...,
        description="PostgreSQL username"
    )
    POSTGRES_PASSWORD: SecretStr = Field(
        ...,
        description="PostgreSQL password"
    )
    POSTGRES_DB: str = Field(
        ...,
        description="PostgreSQL database name"
    )
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # External APIs
    OPENAI_API_KEY: SecretStr = Field(
        ...,
        description="OpenAI API key"
    )
    HUGGINGFACE_TOKEN: Optional[SecretStr] = Field(
        default=None,
        description="Hugging Face API token"
    )

    # Model Configuration
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        description="Model used for text embeddings"
    )
    LLM_MODEL: str = Field(
        default="gpt-4-turbo-preview",
        description="Language model for text generation"
    )

    # Vector Store Configuration
    COLLECTION_NAME: str = Field(
        default="turkish_criminal_law",
        description="Name of the vector store collection"
    )

    # File Paths
    PROJECT_ROOT: Path = Field(
        default=Path(__file__).parent.parent.parent,
        description="Root directory of the project"
    )
    DATA_DIR: Path = Field(
        default=Path(__file__).parent.parent.parent.parent / "data",
        description="Directory containing all data files"
    )
    LAW_JSON_PATH: Path = Field(
        default=Path("data/processed/criminal_law/processed_law.json"),
        description="Path to the processed law JSON file"
    )
    TERMS_JSON_PATH: Path = Field(
        default=Path("data/processed/legal_terms/legal_terms.json"),
        description="Path to the legal terms JSON file"
    )

    # Logging
    LOG_LEVEL: LogLevel = Field(
        default=LogLevel.INFO,
        description="Logging level"
    )
    LOG_FILE: Optional[Path] = Field(
        default=None,
        description="Path to log file"
    )

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        """Construct database URI from components."""
        if isinstance(v, str):
            return v

        password = info.data.get("POSTGRES_PASSWORD")
        if isinstance(password, SecretStr):
            password = password.get_secret_value()

        return str(PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=password,
            host=info.data.get("POSTGRES_SERVER"),
            path=f"/{info.data.get('POSTGRES_DB') or ''}"
        ))

    @field_validator("LOG_FILE")
    def create_log_directory(cls, v: Optional[Path], info: Dict[str, Any]) -> Optional[Path]:
        """Create log directory if it doesn't exist."""
        if v is None:
            v = info.data["PROJECT_ROOT"] / "logs" / "app.log"
        v.parent.mkdir(parents=True, exist_ok=True)
        return v

    @field_validator("LAW_JSON_PATH", "TERMS_JSON_PATH")
    def validate_data_paths(cls, v: Path, info: Dict[str, Any]) -> Path:
        """Validate that data files exist."""
        if "DATA_DIR" not in info.data:
            return v
        
        # Convert relative path to absolute using DATA_DIR
        if not v.is_absolute():
            full_path = info.data["DATA_DIR"] / v
        else:
            full_path = v
            
        if not full_path.exists():
            raise ValueError(f"Data file not found: {full_path}")
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Validate and process CORS origins."""
        if isinstance(v, str):
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            CustomEnvSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        validate_assignment=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings.

    Returns:
        Settings: Application settings instance
    """
    return Settings()

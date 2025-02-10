"""Configuration management for the application."""

import json
import os
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import urlparse


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


@dataclass
class Settings:
    """Application settings with validation."""
    
    # Core settings
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False
    PROJECT_NAME: str = "Turkish Legal AI API"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_FILE: Optional[Path] = None

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = field(default_factory=list)

    # API Keys
    OPENAI_API_KEY: str = ""
    HUGGINGFACE_TOKEN: Optional[str] = None

    # Data paths
    DATA_DIR: Path = Path("data")
    LAW_JSON_PATH: Path = Path("processed/criminal_law/processed_law.json")
    TERMS_JSON_PATH: Path = Path("processed/legal_terms/legal_terms.json")

    # Vector Store
    CHROMA_DB_DIR: Path = Path("chroma_db")
    COLLECTION_NAME: str = "turkish_criminal_law"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    def __post_init__(self):
        """Validate settings after initialization."""
        # Load environment variables
        self._load_env_vars()
        
        # Validate required settings
        self._validate_settings()
        
        # Create necessary directories
        self._create_directories()

    def _load_env_vars(self):
        """Load settings from environment variables."""
        env_file = ".env" if "PYTEST_CURRENT_TEST" not in os.environ else "tests/.env.test"
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

        # Override settings with environment variables
        for field_name in self.__dataclass_fields__:
            env_value = os.getenv(field_name)
            if env_value is not None:
                field_type = type(getattr(self, field_name))
                if field_type == bool:
                    setattr(self, field_name, env_value.lower() == 'true')
                elif field_type == Path:
                    setattr(self, field_name, Path(env_value))
                elif field_type == List[str]:
                    if env_value.startswith('[') and env_value.endswith(']'):
                        try:
                            setattr(self, field_name, json.loads(env_value))
                        except json.JSONDecodeError:
                            setattr(self, field_name, [v.strip() for v in env_value.strip('[]').split(',')])
                    else:
                        setattr(self, field_name, [v.strip() for v in env_value.split(',')])
                else:
                    setattr(self, field_name, field_type(env_value))

    def _validate_settings(self):
        """Validate settings values."""
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set")

        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set")

        # Validate CORS origins
        validated_origins = []
        for origin in self.BACKEND_CORS_ORIGINS:
            try:
                result = urlparse(origin)
                if not all([result.scheme, result.netloc]):
                    raise ValueError
                validated_origins.append(origin)
            except ValueError:
                raise ValueError(f"Invalid CORS origin: {origin}")
        self.BACKEND_CORS_ORIGINS = validated_origins

        # Validate data files
        data_files = [self.LAW_JSON_PATH, self.TERMS_JSON_PATH]
        for file_path in data_files:
            full_path = self.DATA_DIR / file_path
            if not full_path.is_file():
                raise ValueError(f"Data file not found: {full_path}")

    def _create_directories(self):
        """Create necessary directories."""
        # Create log directory if LOG_FILE is set
        if self.LOG_FILE:
            self.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Create ChromaDB directory
        self.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

        # Create data directory
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def clear_settings_cache() -> None:
    """Clear the settings cache."""
    get_settings.cache_clear()

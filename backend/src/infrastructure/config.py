"""Configuration management with validation."""

from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings with validation."""

    # Application
    APP_NAME: str = "Legal AI"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = Field(default=PROJECT_ROOT / "logs" / "app.log")

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        """Construct database URI from components."""
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("LOG_FILE")
    def create_directories(cls, v: Path) -> Path:
        """Ensure directories exist."""
        v.parent.mkdir(parents=True, exist_ok=True)
        return v

    class Config:
        """Pydantic config."""

        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()

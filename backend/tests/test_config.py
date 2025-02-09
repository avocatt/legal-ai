"""Tests for the configuration management system."""

import json
import os
from pathlib import Path
from typing import Generator

import pytest
from pydantic import ValidationError

from app.core.config import Environment, LogLevel, Settings


@pytest.fixture
def mock_env(tmp_path: Path) -> Generator[None, None, None]:
    """Setup test environment variables with temporary paths."""
    original_env = dict(os.environ)
    
    # Create temporary data directories
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    law_dir = data_dir / "processed" / "criminal_law"
    law_dir.mkdir(parents=True)
    terms_dir = data_dir / "processed" / "legal_terms"
    terms_dir.mkdir(parents=True)
    
    # Create mock data files
    (law_dir / "processed_law.json").write_text("{}")
    (terms_dir / "legal_terms.json").write_text("{}")
    
    # Create logs directory
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    
    # Set test environment variables
    os.environ.update({
        "ENVIRONMENT": "development",
        "DEBUG": "true",
        "PROJECT_NAME": "Test API",
        "SECRET_KEY": "test-secret-key",
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_password",
        "POSTGRES_DB": "test_db",
        "OPENAI_API_KEY": "test-api-key",
        "DATA_DIR": str(data_dir),
        "LOG_FILE": str(logs_dir / "test.log"),
        "LAW_JSON_PATH": str(Path("processed/criminal_law/processed_law.json")),
        "TERMS_JSON_PATH": str(Path("processed/legal_terms/legal_terms.json")),
    })
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def test_settings_validation(mock_env):
    """Test settings validation with valid configuration."""
    settings = Settings()
    
    assert settings.ENVIRONMENT == Environment.DEVELOPMENT
    assert settings.DEBUG is True
    assert settings.PROJECT_NAME == "Test API"
    assert settings.SECRET_KEY.get_secret_value() == "test-secret-key"
    assert settings.POSTGRES_USER == "test_user"
    assert settings.POSTGRES_PASSWORD.get_secret_value() == "test_password"
    assert settings.POSTGRES_DB == "test_db"
    assert settings.OPENAI_API_KEY.get_secret_value() == "test-api-key"


def test_missing_required_settings():
    """Test validation error for missing required settings."""
    os.environ.clear()
    
    with pytest.raises(ValidationError) as exc_info:
        Settings()
    
    errors = exc_info.value.errors()
    required_fields = {"SECRET_KEY", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "OPENAI_API_KEY"}
    error_fields = {error["loc"][0] for error in errors}
    assert required_fields.issubset(error_fields)


def test_cors_origins_validation(mock_env):
    """Test CORS origins validation."""
    # Test with JSON string input
    origins = ["http://localhost:3000", "http://localhost:8000"]
    os.environ["BACKEND_CORS_ORIGINS"] = json.dumps(origins)
    settings = Settings()
    assert len(settings.BACKEND_CORS_ORIGINS) == 2
    assert all(str(url).startswith("http://") for url in settings.BACKEND_CORS_ORIGINS)

    # Test with comma-separated string input
    os.environ["BACKEND_CORS_ORIGINS"] = "http://localhost:3000,http://localhost:8000"
    settings = Settings()
    assert len(settings.BACKEND_CORS_ORIGINS) == 2
    assert all(str(url).startswith("http://") for url in settings.BACKEND_CORS_ORIGINS)

    # Test with invalid URL
    os.environ["BACKEND_CORS_ORIGINS"] = "invalid-url"
    with pytest.raises(ValidationError):
        Settings()


def test_database_uri_construction(mock_env):
    """Test database URI construction."""
    settings = Settings()
    db_uri = settings.SQLALCHEMY_DATABASE_URI
    
    assert "postgresql://" in str(db_uri)
    assert settings.POSTGRES_USER in str(db_uri)
    assert settings.POSTGRES_DB in str(db_uri)


def test_log_file_creation(mock_env):
    """Test log file and directory creation."""
    settings = Settings()
    log_file = settings.LOG_FILE
    
    assert log_file.parent.exists()
    assert isinstance(log_file, Path)


def test_environment_enum_validation(mock_env):
    """Test environment enum validation."""
    # Test valid environment
    os.environ["ENVIRONMENT"] = "production"
    settings = Settings()
    assert settings.ENVIRONMENT == Environment.PRODUCTION
    
    # Test invalid environment
    os.environ["ENVIRONMENT"] = "invalid"
    with pytest.raises(ValidationError):
        Settings()


def test_log_level_enum_validation(mock_env):
    """Test log level enum validation."""
    # Test valid log level
    os.environ["LOG_LEVEL"] = "DEBUG"
    settings = Settings()
    assert settings.LOG_LEVEL == LogLevel.DEBUG
    
    # Test invalid log level
    os.environ["LOG_LEVEL"] = "INVALID"
    with pytest.raises(ValidationError):
        Settings()


def test_data_paths_validation(mock_env, tmp_path: Path):
    """Test data paths validation."""
    settings = Settings()
    
    # Test that paths are properly resolved
    assert settings.LAW_JSON_PATH.name == "processed_law.json"
    assert settings.TERMS_JSON_PATH.name == "legal_terms.json"
    
    # Test validation error for non-existent files
    os.environ["DATA_DIR"] = str(tmp_path / "nonexistent")
    with pytest.raises(ValidationError) as exc_info:
        Settings()
    
    errors = exc_info.value.errors()
    assert any("Data file not found" in str(error["msg"]) for error in errors) 
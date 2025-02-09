"""Logging configuration for the application."""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

from .config import settings

# Logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """Configure application logging."""

    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[
            # File handler
            logging.FileHandler(settings.LOG_FILE),
            # Console handler
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Set third-party loggers to WARNING
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin to add logging capabilities to a class."""

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """Initialize the logger with the class name."""
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__name__)

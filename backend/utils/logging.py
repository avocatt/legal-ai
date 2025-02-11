"""Logging configuration for the application."""

import logging
import sys
from typing import Any, Dict

# Configure logging format
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """Set up logging configuration for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log", mode="a"),
        ],
    )


def get_logger(name: str) -> Any:
    """Get a logger instance with the specified name.

    Args:
        name: The name for the logger instance

    Returns:
        Logger instance configured with the application settings
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin to add logging capabilities to a class."""

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        """Initialize the logger with the class name."""
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__name__)

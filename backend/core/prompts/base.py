"""Define base classes for prompt templates."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BasePromptTemplate(ABC):
    """Base class for all prompt templates."""

    def __init__(self, template: str):
        """Initialize the prompt template.

        Args:
            template: The prompt template string
        """
        self.template = template
        self.metadata: Dict[str, Any] = {
            "name": self.__class__.__name__,
            "description": self.__doc__ or "",
            "version": "1.0",
        }

    @abstractmethod
    def format(self, **kwargs) -> str:
        """Format the template with the given arguments.

        Args:
            **kwargs: Keyword arguments to format the template

        Returns:
            str: The formatted prompt
        """
        pass

    @abstractmethod
    def validate_inputs(self, **kwargs) -> bool:
        """Validate the input arguments.

        Args:
            **kwargs: Keyword arguments to validate

        Returns:
            bool: True if inputs are valid, False otherwise
        """
        pass

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the prompt template.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Optional[Any]:
        """Get metadata value.

        Args:
            key: Metadata key

        Returns:
            Optional[Any]: Metadata value if exists, None otherwise
        """
        return self.metadata.get(key)

    def __str__(self) -> str:
        """Get string representation of the prompt template."""
        return f"{self.__class__.__name__}(template={self.template})"

"""API request and response schemas."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class QuestionRequest:
    """Request model for question answering endpoint."""
    question: str
    metadata_filter: Optional[Dict[str, str]] = None
    n_results: int = 5

    def __post_init__(self):
        """Validate the request data."""
        if not isinstance(self.question, str) or not 1 <= len(self.question) <= 1000:
            raise ValueError("Question must be a string between 1 and 1000 characters")
        
        if self.metadata_filter is not None and not isinstance(self.metadata_filter, dict):
            raise ValueError("metadata_filter must be a dictionary")
        
        if not isinstance(self.n_results, int) or not 1 <= self.n_results <= 10:
            raise ValueError("n_results must be an integer between 1 and 10")


@dataclass
class SearchResult:
    """Model representing a single search result."""
    id: str
    content: str
    metadata: Dict[str, Any]
    distance: Optional[float] = None

    def __post_init__(self):
        """Validate the search result data."""
        if not isinstance(self.id, str):
            raise ValueError("id must be a string")
        if not isinstance(self.content, str):
            raise ValueError("content must be a string")
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dictionary")


@dataclass
class QuestionResponse:
    """Response model for question answering endpoint."""
    answer: str
    sources: List[SearchResult]
    processing_time: float
    confidence_score: Optional[float] = None

    def __post_init__(self):
        """Validate the response data."""
        if not isinstance(self.answer, str):
            raise ValueError("answer must be a string")
        if not isinstance(self.sources, list):
            raise ValueError("sources must be a list")
        if not isinstance(self.processing_time, (int, float)):
            raise ValueError("processing_time must be a number")
        if self.confidence_score is not None and not isinstance(self.confidence_score, float):
            raise ValueError("confidence_score must be a float if provided") 
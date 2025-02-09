"""API request and response models.

This module defines the Pydantic models used for API request/response validation
and serialization in the question answering system.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Request model for question answering endpoint.

    Attributes:
        question (str): The question text, between 1-1000 characters
        metadata_filter (Optional[Dict[str, str]]): Optional filters for specific content
        n_results (Optional[int]): Number of source documents to return (1-10)
    """

    question: str = Field(..., min_length=1, max_length=1000)
    metadata_filter: Optional[Dict[str, str]] = None
    n_results: Optional[int] = Field(default=5, ge=1, le=10)


class SearchResult(BaseModel):
    """Model representing a single search result from the vector store.

    Attributes:
        id (str): Unique identifier of the document
        content (str): Text content of the document
        metadata (Dict[str, Any]): Additional metadata about the document
        distance (Optional[float]): Similarity distance score if available
    """

    id: str
    content: str
    metadata: Dict[str, Any]
    distance: Optional[float] = None


class QuestionResponse(BaseModel):
    """Response model for question answering endpoint.

    Attributes:
        answer (str): The generated answer text
        confidence_score (Optional[float]): Confidence score of the answer
        sources (list[SearchResult]): Relevant source documents used
        processing_time (float): Time taken to process the request in seconds
    """

    answer: str
    confidence_score: Optional[float] = None
    sources: list[SearchResult]
    processing_time: float

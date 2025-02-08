"""Request models for the Turkish Legal AI API.

This module defines Pydantic models for validating and documenting API request payloads.
"""

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Request model for submitting a legal question."""

    question: str = Field(
        ...,
        description="The legal question to be answered",
        min_length=10,
        max_length=1000,
    )

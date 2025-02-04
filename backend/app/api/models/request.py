from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    metadata_filter: Optional[Dict[str, str]] = None
    n_results: Optional[int] = Field(default=5, ge=1, le=10)


class SearchResult(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    distance: Optional[float] = None


class QuestionResponse(BaseModel):
    answer: str
    confidence_score: Optional[float] = None
    sources: list[SearchResult]
    processing_time: float

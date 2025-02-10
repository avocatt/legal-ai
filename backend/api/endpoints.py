"""Question answering API endpoints.

This module provides FastAPI endpoints for the question answering system,
handling user queries about Turkish Criminal Law and returning relevant answers.
"""

import logging
from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from core.rag_system import TurkishLegalRAG
from .schemas import QuestionRequest, QuestionResponse, SearchResult

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/question")
async def ask_question(request_data: dict) -> dict:
    """Process a question about Turkish Criminal Law and return an answer.

    Args:
        request_data: The question request containing:
            - question: The question text (1-1000 characters)
            - metadata_filter: Optional filters for specific sections of law
            - n_results: Number of source documents to return (1-10)

    Returns:
        dict: The answer and relevant source documents

    Raises:
        HTTPException: If there's an error processing the question
    """
    try:
        # Convert request data to QuestionRequest dataclass
        request = QuestionRequest(**request_data)
        logger.info(f"Received question request: {request}")

        # Process the request using RAG system directly
        rag_system = TurkishLegalRAG()
        result = await rag_system.answer_question(
            question=request.question,
            metadata_filter=request.metadata_filter,
            n_results=request.n_results,
        )

        # Convert result to QuestionResponse dataclass
        sources = [SearchResult(**source) for source in result["sources"]]
        response = QuestionResponse(
            answer=result["answer"],
            sources=sources,
            processing_time=result["processing_time"],
            confidence_score=result.get("confidence_score")
        )

        logger.info("Successfully generated answer")
        return jsonable_encoder(asdict(response))
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

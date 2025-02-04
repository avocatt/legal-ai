from fastapi import APIRouter, HTTPException
import logging
from ...services.qa_service import qa_service
from ..models.request import QuestionRequest, QuestionResponse

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about Turkish Criminal Law.

    - **question**: The question text (1-1000 characters)
    - **metadata_filter**: Optional filters for specific sections of law
    - **n_results**: Number of source documents to return (1-10)
    """
    logger.info(f"Received question request: {request}")
    try:
        result = await qa_service.get_answer(
            question=request.question,
            metadata_filter=request.metadata_filter,
            n_results=request.n_results
        )
        logger.info("Successfully generated answer")
        return result
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

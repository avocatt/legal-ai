"""FastAPI application entry point for the Turkish Legal AI API."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter

from src.core.config import get_settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create API router
api_router = APIRouter()

# Import and include endpoints
from src.api.endpoints.qa import router as qa_router
api_router.include_router(qa_router, prefix="/qa", tags=["qa"])

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Initialize application state on startup."""
    logger.info("Starting up the application...")
    logger.info("Application startup complete")
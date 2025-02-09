"""FastAPI application entry point for the Turkish Legal AI API.

This module initializes and configures the FastAPI application,
setting up middleware, routers, and application state management.
"""

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

# Application state to track initialization
app.state.is_initialized = False


@app.on_event("startup")
async def startup_event():
    """Initialize application state on startup.

    This function runs when the FastAPI application starts up,
    performing any necessary initialization tasks.
    """
    logger.info("Starting up the application...")
    # Mark as initialized - in production you might want to add more checks
    app.state.is_initialized = True
    logger.info("Application startup complete")


@app.get("/health")
async def health_check():
    """Check the health status of the application.

    Returns:
        dict: Health status information
            - status: "healthy" if the application is ready
            - status: "initializing" if the application is still starting up

    Response Codes:
        200: Application is healthy
        503: Application is still initializing
    """
    if not app.state.is_initialized:
        logger.warning("Health check failed: Application not fully initialized")
        return {"status": "initializing"}, 503

    logger.info("Health check passed: Application is healthy")
    return {"status": "healthy"} 
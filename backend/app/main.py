from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .core.config import get_settings
from .api.endpoints import qa

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(qa.router, prefix=settings.API_V1_STR)

# Application state to track initialization
app.state.is_initialized = False


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    # Mark as initialized - in production you might want to add more checks
    app.state.is_initialized = True
    logger.info("Application startup complete")


@app.get("/health")
async def health_check():
    """Enhanced health check endpoint that ensures the application is fully initialized."""
    if not app.state.is_initialized:
        logger.warning(
            "Health check failed: Application not fully initialized")
        return {"status": "initializing"}, 503

    logger.info("Health check passed: Application is healthy")
    return {"status": "healthy"}

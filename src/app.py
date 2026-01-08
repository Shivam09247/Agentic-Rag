"""
FastAPI application factory and configuration.
Production-ready setup with versioning, error handling, and middleware.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.core import settings, get_logger, ConfigurationError
from src.memory.database import get_database_service
from src.api.router import api_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Runs on startup and shutdown.
    """
    # Startup
    logger.info("Starting Agentic RAG API...")
    
    try:
        # Initialize database service
        db_service = get_database_service()
        is_healthy = await db_service.health_check()
        
        if is_healthy:
            logger.info("✓ Database connection established")
        else:
            logger.warning("⚠ Database connection failed - using degraded mode")
    
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise ConfigurationError(f"Failed to initialize: {e}")
    
    logger.info("✓ Agentic RAG API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic RAG API...")
    logger.info("✓ Agentic RAG API stopped")


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Agentic RAG API",
        description="Production-ready Retrieval-Augmented Generation with session memory",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(api_router, prefix="/api")
    
    # Exception handlers
    @app.exception_handler(ConfigurationError)
    async def configuration_error_handler(request: Request, exc: ConfigurationError):
        logger.error(f"Configuration error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Configuration Error",
                "message": str(exc),
                "type": "configuration_error"
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "type": type(exc).__name__
            }
        )
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint - API information."""
        return {
            "name": "Agentic RAG API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs"
        }
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        db_service = get_database_service()
        db_healthy = await db_service.health_check()
        
        return {
            "status": "healthy" if db_healthy else "degraded",
            "database": "connected" if db_healthy else "disconnected",
            "version": "1.0.0"
        }
    
    logger.info("FastAPI application created")
    return app


# Create application instance
app = create_application()

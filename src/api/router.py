"""
Main API router - aggregates all API versions.
"""

from fastapi import APIRouter
from src.api.v1.router import api_v1_router

# Create main API router
api_router = APIRouter()

# Include versioned routers
api_router.include_router(api_v1_router, prefix="/v1", tags=["API v1"])

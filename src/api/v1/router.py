"""
API v1 router - aggregates all v1 endpoints.
"""

from fastapi import APIRouter
from src.api.v1 import query, session, documents

# Create API v1 router
api_v1_router = APIRouter()

# Include sub-routers
api_v1_router.include_router(query.router, prefix="/query", tags=["Query"])
api_v1_router.include_router(session.router, prefix="/sessions", tags=["Sessions"])
api_v1_router.include_router(documents.router, prefix="/documents", tags=["Documents"])

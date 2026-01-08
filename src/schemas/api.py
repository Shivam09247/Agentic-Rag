"""
API schemas - BACKWARD COMPATIBILITY LAYER
All models have been reorganized into request.py, response.py, and agent_io.py
This file re-exports them for backward compatibility.
"""

# Request models
from src.schemas.request import (
    QueryRequest,
    SessionCreateRequest,
    DocumentUploadRequest,
)

# Response models
from src.schemas.response import (
    QueryResponse,
    SessionResponse,
    ConversationHistoryResponse,
    ErrorResponse,
    HealthResponse,
    DocumentUploadResponse,
)

__all__ = [
    # Requests
    "QueryRequest",
    "SessionCreateRequest",
    "DocumentUploadRequest",
    # Responses
    "QueryResponse",
    "SessionResponse",
    "ConversationHistoryResponse",
    "ErrorResponse",
    "HealthResponse",
    "DocumentUploadResponse",
]

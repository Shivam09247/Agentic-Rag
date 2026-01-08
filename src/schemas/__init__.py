"""
Schemas package - Pydantic models for requests, responses, and agent I/O.
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

# Agent I/O models
from src.schemas.agent_io import (
    AgentInput,
    AgentOutput,
    QueryRewriteOutput,
    NeedsInfoOutput,
    SourceSelectionOutput,
    RetrievalOutput,
    AnswerEvaluationOutput,
)

# Backward compatibility - keep api.py imports
from src.schemas.api import *

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
    # Agent I/O
    "AgentInput",
    "AgentOutput",
    "QueryRewriteOutput",
    "NeedsInfoOutput",
    "SourceSelectionOutput",
    "RetrievalOutput",
    "AnswerEvaluationOutput",
]

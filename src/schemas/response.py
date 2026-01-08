"""
Response schemas for API endpoints.
All outgoing response models.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    """Response model for RAG query."""
    answer: str = Field(..., description="Generated answer")
    thread_id: str = Field(..., description="Session thread ID")
    query: str = Field(..., description="Original query")
    rewritten_query: Optional[str] = Field(None, description="Rewritten query")
    needs_retrieval: bool = Field(..., description="Whether retrieval was used")
    selected_source: Optional[str] = Field(None, description="Source used for retrieval")
    answer_is_relevant: bool = Field(..., description="Answer quality evaluation")
    iteration: int = Field(..., description="Number of iterations taken")
    message_count: int = Field(..., description="Total messages in conversation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Python is a high-level programming language...",
                "thread_id": "user_session_123",
                "query": "What is Python?",
                "rewritten_query": "What is Python programming language?",
                "needs_retrieval": True,
                "selected_source": "vector_db",
                "answer_is_relevant": True,
                "iteration": 1,
                "message_count": 4
            }
        }


class SessionResponse(BaseModel):
    """Response model for session operations."""
    thread_id: str = Field(..., description="Session thread ID")
    user_id: Optional[str] = Field(None, description="User identifier")
    message_count: int = Field(..., description="Number of messages in session")
    created_at: str = Field(..., description="Session creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "thread_id": "abc123def456",
                "user_id": "user_123",
                "message_count": 4,
                "created_at": "2026-01-08T10:30:00"
            }
        }


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""
    thread_id: str = Field(..., description="Session thread ID")
    message_count: int = Field(..., description="Total messages")
    messages: List[Dict[str, Any]] = Field(..., description="Message history")
    
    class Config:
        json_schema_extra = {
            "example": {
                "thread_id": "abc123def456",
                "message_count": 4,
                "messages": [
                    {"role": "user", "content": "What is Python?"},
                    {"role": "assistant", "content": "Python is..."}
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid request data",
                "details": {}
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    database: str = Field(..., description="Database connection status")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "database": "connected",
                "version": "1.0.0"
            }
        }


class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    success: bool = Field(..., description="Upload success status")
    filename: str = Field(..., description="Uploaded filename")
    document_id: Optional[str] = Field(None, description="Document ID in vector store")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "document.txt",
                "document_id": "doc_123456",
                "message": "Document uploaded and indexed successfully"
            }
        }

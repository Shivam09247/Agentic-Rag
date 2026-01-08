"""
Request schemas for API endpoints.
All incoming request models.
"""

from typing import Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for RAG query."""
    query: str = Field(..., description="User query", min_length=1, max_length=1000)
    thread_id: Optional[str] = Field(None, description="Session thread ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="User identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is Python?",
                "thread_id": "user_session_123",
                "user_id": "user_123"
            }
        }


class SessionCreateRequest(BaseModel):
    """Request model for creating a new session."""
    user_id: Optional[str] = Field(None, description="User identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123"
            }
        }


class DocumentUploadRequest(BaseModel):
    """Request model for document upload."""
    filename: str = Field(..., description="Document filename")
    content: str = Field(..., description="Document content")
    metadata: Optional[dict] = Field(None, description="Optional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "document.txt",
                "content": "This is the document content...",
                "metadata": {"author": "John Doe", "date": "2026-01-08"}
            }
        }

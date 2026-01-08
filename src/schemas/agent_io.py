"""
Agent input/output schemas.
Internal schemas for agent communication and state management.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    """Input schema for agent invocations."""
    query: str = Field(..., description="Query to process")
    context: Optional[str] = Field(None, description="Additional context")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")


class AgentOutput(BaseModel):
    """Output schema for agent results."""
    result: str = Field(..., description="Agent result")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Output metadata")


class QueryRewriteOutput(BaseModel):
    """Output from query rewriter agent."""
    rewritten_query: str = Field(..., description="Rewritten query")
    original_query: str = Field(..., description="Original query")
    reason: Optional[str] = Field(None, description="Reason for rewrite")


class NeedsInfoOutput(BaseModel):
    """Output from needs-more-info agent."""
    needs_retrieval: bool = Field(..., description="Whether retrieval is needed")
    reason: str = Field(..., description="Reasoning for decision")


class SourceSelectionOutput(BaseModel):
    """Output from source selector agent."""
    selected_source: Literal["vector_database", "web_search", "tools_api"] = Field(
        ..., description="Selected information source"
    )
    reason: str = Field(..., description="Reasoning for selection")


class RetrievalOutput(BaseModel):
    """Output from retrieval operations."""
    documents: List[str] = Field(..., description="Retrieved documents")
    source: str = Field(..., description="Source of retrieval")
    metadata: List[Dict[str, Any]] = Field(default_factory=list, description="Document metadata")


class AnswerEvaluationOutput(BaseModel):
    """Output from answer evaluator agent."""
    is_relevant: bool = Field(..., description="Whether answer is relevant")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Evaluation confidence")
    reason: str = Field(..., description="Reasoning for evaluation")
    suggestions: Optional[str] = Field(None, description="Suggestions for improvement")

"""
Agent State - Defines the state schema for the Agentic RAG workflow
"""
from typing import TypedDict, List, Optional, Dict, Any, Literal, Annotated
from pydantic import BaseModel, Field
from datetime import datetime
import operator


class Document(BaseModel):
    """Retrieved document with metadata"""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: float = 0.0
    source: str = "unknown"


class ToolCall(BaseModel):
    """Tool invocation record"""
    tool_name: str
    tool_input: Dict[str, Any]
    tool_output: Optional[str] = None
    success: bool = True
    error: Optional[str] = None
    execution_time: float = 0.0


class Message(BaseModel):
    """Chat message"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentState(TypedDict):
    """
    State schema for the Agentic RAG workflow
    
    This state flows through the LangGraph nodes and maintains
    all information needed for the RAG pipeline.
    """
    # Input
    query: str  # Original user query
    session_id: str  # Session identifier
    user_id: Optional[str]  # User identifier
    
    # Query Processing
    rewritten_query: str  # Query after rewriting
    query_intent: str  # Detected intent (factual, exploratory, etc.)
    
    # Decision Making
    needs_retrieval: bool  # Whether retrieval is needed
    selected_sources: List[str]  # Sources to query: ["vector_db", "web_search", "tools"]
    
    # Retrieval
    retrieved_documents: List[Dict]  # Retrieved documents
    context: str  # Formatted context string
    
    # Tool Execution
    planned_tools: List[Dict]  # Tools to execute
    tool_results: Annotated[List[Dict], operator.add]  # Tool execution results
    
    # Generation
    response: str  # Generated response
    
    # Validation
    is_valid: bool  # Whether response passed validation
    validation_feedback: str  # Feedback from validator
    relevance_score: float  # Relevance score 0-1
    
    # Control Flow
    iteration: int  # Current iteration number
    max_iterations: int  # Maximum iterations allowed
    should_retry: bool  # Whether to retry generation
    retry_reason: str  # Reason for retry
    
    # History
    messages: Annotated[List[Dict], operator.add]  # Conversation history
    
    # Metadata
    error: Optional[str]  # Error message if any
    metadata: Dict[str, Any]  # Additional metadata


def create_initial_state(
    query: str,
    session_id: str,
    user_id: Optional[str] = None,
    max_iterations: int = 5
) -> AgentState:
    """Create initial state for a new query"""
    return AgentState(
        # Input
        query=query,
        session_id=session_id,
        user_id=user_id,
        
        # Query Processing
        rewritten_query="",
        query_intent="",
        
        # Decision Making
        needs_retrieval=True,
        selected_sources=[],
        
        # Retrieval
        retrieved_documents=[],
        context="",
        
        # Tool Execution
        planned_tools=[],
        tool_results=[],
        
        # Generation
        response="",
        
        # Validation
        is_valid=False,
        validation_feedback="",
        relevance_score=0.0,
        
        # Control Flow
        iteration=0,
        max_iterations=max_iterations,
        should_retry=False,
        retry_reason="",
        
        # History
        messages=[{"role": "user", "content": query}],
        
        # Metadata
        error=None,
        metadata={}
    )


class QueryClassification(BaseModel):
    """Classification of user query"""
    intent: Literal["factual", "exploratory", "comparison", "procedural", "opinion"]
    complexity: Literal["simple", "moderate", "complex"]
    requires_retrieval: bool
    requires_tools: bool
    suggested_sources: List[str]


class RetrievalDecision(BaseModel):
    """Decision about retrieval strategy"""
    should_retrieve: bool = True
    sources: List[Literal["vector_db", "web_search", "api", "tools"]] = ["vector_db"]
    reasoning: str = ""


class ValidationResult(BaseModel):
    """Result of response validation"""
    is_valid: bool
    relevance_score: float = Field(ge=0, le=1)
    completeness_score: float = Field(ge=0, le=1)
    faithfulness_score: float = Field(ge=0, le=1)
    feedback: str
    should_retry: bool
    retry_suggestion: str = ""

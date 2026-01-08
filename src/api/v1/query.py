"""
Query endpoints - Main RAG functionality.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from langchain_core.messages import HumanMessage, AIMessage

from src.schemas.api import QueryRequest, QueryResponse
from src.api.dependencies import verify_api_key, get_thread_id
from src.graph.rag_graph import run_agentic_rag
from src.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def process_query(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
) -> QueryResponse:
    """
    Process a user query through the Agentic RAG system.
    
    - **query**: User's question or request
    - **thread_id**: Optional session ID for conversation continuity
    - **user_id**: Optional user identifier
    
    Returns the generated answer with metadata.
    """
    try:
        # Get or create thread ID
        thread_id = get_thread_id(request.thread_id, request.user_id)
        
        logger.info(f"Processing query: '{request.query}' (thread: {thread_id[:16]}...)")
        
        # Run RAG workflow
        result = run_agentic_rag(
            query=request.query,
            thread_id=thread_id
        )
        
        # Count messages
        messages = result.get("messages", [])
        message_count = len(messages)
        
        # Build response
        response = QueryResponse(
            answer=result.get("answer", "No answer generated"),
            thread_id=thread_id,
            query=result.get("original_query", request.query),
            rewritten_query=result.get("rewritten_query"),
            needs_retrieval=result.get("needs_retrieval", False),
            selected_source=result.get("selected_source"),
            answer_is_relevant=result.get("answer_is_relevant", False),
            iteration=result.get("iteration", 0),
            message_count=message_count
        )
        
        logger.info(f"Query processed successfully (thread: {thread_id[:16]}...)")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def query_health():
    """Health check for query service."""
    return {
        "status": "healthy",
        "service": "query"
    }

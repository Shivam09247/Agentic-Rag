"""
Session management endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from src.schemas.api import SessionCreateRequest, SessionResponse, ConversationHistoryResponse
from src.api.dependencies import verify_api_key, get_db_service
from src.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: SessionCreateRequest,
    api_key: str = Depends(verify_api_key)
) -> SessionResponse:
    """
    Create a new conversation session.
    
    - **user_id**: Optional user identifier
    
    Returns a new session with thread_id.
    """
    try:
        from src.session.manager import SessionManager
        
        session_manager = SessionManager()
        thread_id = session_manager.create_session(user_id=request.user_id)
        
        session_info = session_manager.get_session_info(thread_id)
        
        logger.info(f"Created new session: {thread_id[:16]}...")
        
        return SessionResponse(
            thread_id=thread_id,
            user_id=request.user_id,
            message_count=session_info.get("message_count", 0),
            created_at=session_info.get("created_at", "")
        )
        
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/{thread_id}", response_model=SessionResponse, status_code=status.HTTP_200_OK)
async def get_session(
    thread_id: str,
    api_key: str = Depends(verify_api_key)
) -> SessionResponse:
    """
    Get information about a specific session.
    
    - **thread_id**: Session thread identifier
    
    Returns session metadata.
    """
    try:
        from src.session.manager import SessionManager
        
        session_manager = SessionManager()
        session_info = session_manager.get_session_info(thread_id)
        
        if not session_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {thread_id}"
            )
        
        return SessionResponse(
            thread_id=thread_id,
            user_id=session_info.get("user_id"),
            message_count=session_info.get("message_count", 0),
            created_at=session_info.get("created_at", "")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session: {str(e)}"
        )


@router.get("/{thread_id}/history", response_model=ConversationHistoryResponse, status_code=status.HTTP_200_OK)
async def get_conversation_history(
    thread_id: str,
    limit: int = 50,
    api_key: str = Depends(verify_api_key)
) -> ConversationHistoryResponse:
    """
    Get conversation history for a session.
    
    - **thread_id**: Session thread identifier
    - **limit**: Maximum number of messages to return
    
    Returns conversation messages.
    """
    try:
        from src.session.manager import SessionManager
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        
        session_manager = SessionManager()
        history = session_manager.get_conversation_history(thread_id, limit=limit)
        
        # Format messages
        messages = []
        for snapshot in history:
            state_messages = snapshot.values.get("messages", [])
            for msg in state_messages:
                if isinstance(msg, HumanMessage):
                    messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    messages.append({"role": "assistant", "content": msg.content})
                elif isinstance(msg, SystemMessage):
                    messages.append({"role": "system", "content": msg.content})
        
        return ConversationHistoryResponse(
            thread_id=thread_id,
            message_count=len(messages),
            messages=messages
        )
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation history: {str(e)}"
        )


@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    thread_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Delete a session and its conversation history.
    
    - **thread_id**: Session thread identifier
    """
    try:
        from src.session.manager import SessionManager
        
        session_manager = SessionManager()
        success = session_manager.clear_thread(thread_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {thread_id}"
            )
        
        logger.info(f"Deleted session: {thread_id[:16]}...")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.get("", response_model=List[SessionResponse], status_code=status.HTTP_200_OK)
async def list_sessions(
    api_key: str = Depends(verify_api_key)
) -> List[SessionResponse]:
    """
    List all active sessions.
    
    Returns list of active sessions.
    """
    try:
        from src.session.manager import SessionManager
        
        session_manager = SessionManager()
        sessions = session_manager.list_active_sessions()
        
        return [
            SessionResponse(
                thread_id=session["thread_id"],
                user_id=session.get("user_id"),
                message_count=session.get("message_count", 0),
                created_at=session.get("created_at", "")
            )
            for session in sessions
        ]
        
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )

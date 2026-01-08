"""
Shared dependencies for API endpoints.
"""

from typing import Optional
from fastapi import Header, HTTPException, status

from src.core import get_logger
from src.memory.database import get_database_service

logger = get_logger(__name__)


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from request headers.
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        Verified API key
        
    Raises:
        HTTPException: If API key is invalid
    """
    # TODO: Implement proper API key verification
    # For now, accept any key or no key (development mode)
    
    if x_api_key:
        logger.debug(f"API key provided: {x_api_key[:8]}...")
        return x_api_key
    
    logger.debug("No API key provided (development mode)")
    return "dev_mode"


async def get_db_service():
    """
    Get database service dependency.
    
    Returns:
        DatabaseService instance
    """
    return get_database_service()


def get_thread_id(thread_id: Optional[str], user_id: Optional[str]) -> str:
    """
    Generate thread ID from user input.
    
    Args:
        thread_id: Provided thread ID
        user_id: User identifier
        
    Returns:
        Thread ID to use for session
    """
    if thread_id:
        return thread_id
    
    if user_id:
        return f"user_{user_id}_session"
    
    # Generate default thread ID
    from uuid import uuid4
    return str(uuid4())

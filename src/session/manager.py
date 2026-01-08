"""
Session management utilities.
Handles session creation, retrieval, and cleanup.
"""

from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime

from langchain_core.runnables import RunnableConfig

from src.core import get_logger
from src.memory.database import get_database_service

logger = get_logger(__name__)


class SessionManager:
    """
    Manages conversation sessions and their lifecycle.
    """
    
    def __init__(self):
        """Initialize session manager."""
        self.db_service = get_database_service()
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """
        Create a new conversation session.
        
        Args:
            user_id: Optional user identifier
            
        Returns:
            New thread_id for the session
        """
        thread_id = str(uuid4())
        logger.info(f"Created new session: {thread_id[:16]}... (user: {user_id})")
        return thread_id
    
    def get_session_info(self, thread_id: str) -> Dict[str, Any]:
        """
        Get information about a session.
        
        Args:
            thread_id: Session identifier
            
        Returns:
            Session information dictionary
        """
        try:
            checkpointer = self.db_service.get_checkpointer()
            
            # Get latest checkpoint
            config = {"configurable": {"thread_id": thread_id}}
            checkpoint = checkpointer.get(config)
            
            if not checkpoint:
                return {
                    "thread_id": thread_id,
                    "message_count": 0,
                    "created_at": datetime.now().isoformat()
                }
            
            # Count messages
            messages = checkpoint.get("channel_values", {}).get("messages", [])
            message_count = len(messages) if messages else 0
            
            return {
                "thread_id": thread_id,
                "message_count": message_count,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return {
                "thread_id": thread_id,
                "message_count": 0,
                "created_at": datetime.now().isoformat()
            }
    
    def get_conversation_history(self, thread_id: str, limit: int = 50) -> List[Any]:
        """
        Get conversation history for a session.
        
        Args:
            thread_id: Session identifier
            limit: Maximum number of checkpoints to return
            
        Returns:
            List of checkpoint snapshots
        """
        try:
            checkpointer = self.db_service.get_checkpointer()
            config = {"configurable": {"thread_id": thread_id}}
            
            # Get checkpoints
            history = []
            for snapshot in checkpointer.list(config, limit=limit):
                history.append(snapshot)
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def clear_thread(self, thread_id: str) -> bool:
        """
        Clear a conversation thread.
        
        Args:
            thread_id: Session identifier
            
        Returns:
            True if successful
        """
        try:
            # Note: MongoDBSaver doesn't have a built-in delete method
            # You would need to implement this directly on the MongoDB collection
            logger.info(f"Clearing thread: {thread_id[:16]}...")
            
            from pymongo import MongoClient
            from src.core import settings
            
            # Connect to MongoDB
            connection_uri = self.db_service._build_connection_uri()
            client = MongoClient(connection_uri)
            db = client[settings.MONGODB_DB]
            
            # Delete checkpoints for this thread
            result = db.checkpoints.delete_many({"thread_id": thread_id})
            
            logger.info(f"Deleted {result.deleted_count} checkpoints for thread {thread_id[:16]}...")
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error clearing thread: {e}")
            return False
    
    def list_active_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all active sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session information dictionaries
        """
        try:
            from pymongo import MongoClient
            from src.core import settings
            
            # Connect to MongoDB
            connection_uri = self.db_service._build_connection_uri()
            client = MongoClient(connection_uri)
            db = client[settings.MONGODB_DB]
            
            # Get unique thread_ids
            pipeline = [
                {"$group": {"_id": "$thread_id"}},
                {"$limit": limit}
            ]
            
            thread_ids = [doc["_id"] for doc in db.checkpoints.aggregate(pipeline)]
            
            # Get session info for each thread
            sessions = []
            for thread_id in thread_ids:
                session_info = self.get_session_info(thread_id)
                if session_info:
                    sessions.append(session_info)
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error listing active sessions: {e}")
            return []

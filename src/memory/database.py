"""
Database service for MongoDB session memory management.
Handles connection and session checkpointing.
"""

from typing import Optional
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from src.core import settings, get_logger, ConfigurationError

logger = get_logger(__name__)


class DatabaseService:
    """Service for managing MongoDB connections and session memory."""
    
    def __init__(self):
        """Initialize database service with connection details from settings."""
        self.db_uri = self._build_connection_uri()
        self._checkpointer: Optional[MongoDBSaver] = None
        self._client: Optional[MongoClient] = None
        logger.info("DatabaseService initialized")
    
    def _build_connection_uri(self) -> str:
        """Build MongoDB connection URI from settings."""
        if settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD:
            uri = (
                f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}"
                f"@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"
            )
            logger.debug(f"Database URI built: mongodb://{settings.MONGODB_USERNAME}:***@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}")
        else:
            uri = f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"
            logger.debug(f"Database URI built: mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}")
        return uri
    
    def get_checkpointer(self):
        """
        Get MongoDB checkpointer instance.
        
        Returns:
            MongoDBSaver: Checkpointer instance for LangGraph
            
        Example:
            >>> db_service = DatabaseService()
            >>> checkpointer = db_service.get_checkpointer()
            >>> graph = builder.compile(checkpointer=checkpointer)
        """
        if self._checkpointer is None:
            try:
                logger.info("Creating MongoDB checkpointer connection")
                # Create persistent MongoDB client with serverSelectionTimeoutMS
                self._client = MongoClient(
                    self.db_uri,
                    serverSelectionTimeoutMS=5000
                )
                # Test connection
                self._client.admin.command('ping')
                logger.info("MongoDB connection successful")
                
                # Create MongoDB database reference
                db = self._client[settings.MONGODB_DB]
                # Create saver with the database and specify collection prefix
                self._checkpointer = MongoDBSaver(
                    db,
                    collection_name="checkpoints"
                )
                logger.info("MongoDB checkpointer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize MongoDB checkpointer: {str(e)}")
                raise ConfigurationError(f"Database connection failed: {str(e)}")
        
        return self._checkpointer
    
    async def health_check(self) -> bool:
        """
        Check if database connection is healthy.
        
        Returns:
            bool: True if database is accessible, False otherwise
        """
        try:
            checkpointer = self.get_checkpointer()
            # If we can create checkpointer, connection is healthy
            logger.debug("Database health check passed")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False


# Singleton instance
_db_service_instance: Optional[DatabaseService] = None


def get_database_service() -> DatabaseService:
    """
    Get or create singleton DatabaseService instance.
    
    Returns:
        DatabaseService: Singleton database service instance
    """
    global _db_service_instance
    if _db_service_instance is None:
        _db_service_instance = DatabaseService()
    return _db_service_instance

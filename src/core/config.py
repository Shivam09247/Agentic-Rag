"""Configuration settings for Agentic RAG system."""

import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    groq_api_key: str = ""
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.4
    
    # OpenAI Configuration (for embeddings)
    openai_api_key: str = ""
    
    # Embedding Configuration
    embedding_model: str = "text-embedding-3-small"
    
    # Vector Store Configuration
    vector_store_type: Literal["chroma", "faiss", "pinecone"] = "chroma"
    chroma_persist_dir: str = "./data/chroma"
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    
    # Web Search Configuration
    tavily_api_key: str = ""
    serpapi_api_key: str = ""
    
    # RAG Configuration
    max_iterations: int = 3
    retrieval_top_k: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Logging
    log_level: str = "INFO"
    
    # MongoDB Configuration (for session persistence)
    mongodb_uri: str = "mongodb://localhost:27017/"  # Deprecated: use individual settings below
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_username: str = ""
    mongodb_password: str = ""
    mongodb_db: str = "agentic_rag"
    mongodb_collection: str = "checkpoints"
    
    # Convenience properties for backward compatibility
    @property
    def MONGODB_HOST(self) -> str:
        return self.mongodb_host
    
    @property
    def MONGODB_PORT(self) -> int:
        return self.mongodb_port
    
    @property
    def MONGODB_USERNAME(self) -> str:
        return self.mongodb_username
    
    @property
    def MONGODB_PASSWORD(self) -> str:
        return self.mongodb_password
    
    @property
    def MONGODB_DB(self) -> str:
        return self.mongodb_db
    
    # Session Configuration
    session_ttl_hours: int = 24  # Session time-to-live in hours
    max_session_messages: int = 50  # Maximum messages to keep in session
    max_context_messages: int = 10  # Maximum messages sent to LLM (sliding window)
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"
    documents_dir: Path = data_dir / "documents"
    embeddings_dir: Path = data_dir / "embeddings"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

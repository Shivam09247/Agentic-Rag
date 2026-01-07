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

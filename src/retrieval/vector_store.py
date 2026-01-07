"""Vector store management for document retrieval."""

import hashlib
import json
from pathlib import Path
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from src.config.settings import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class VectorStoreManager:
    """Manages vector store operations for document retrieval."""
    
    def __init__(self):
        """Initialize the vector store manager."""
        # Use free HuggingFace embeddings instead of OpenAI
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store: Chroma | None = None
        self.index_metadata_file = Path(settings.chroma_persist_dir) / "indexed_files.json"
    
    def _get_file_hash(self, filepath: str) -> str:
        """
        Generate MD5 hash of file content.
        
        Args:
            filepath: Path to file
            
        Returns:
            MD5 hash string
        """
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _load_indexed_files(self) -> dict:
        """
        Load metadata of already indexed files.
        
        Returns:
            Dictionary mapping file paths to their hashes
        """
        if self.index_metadata_file.exists():
            with open(self.index_metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_indexed_files(self, metadata: dict) -> None:
        """
        Save metadata of indexed files.
        
        Args:
            metadata: Dictionary mapping file paths to their hashes
        """
        self.index_metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
    def initialize_vector_store(self) -> None:
        """Initialize or load existing vector store."""
        logger.info("Initializing vector store...")
        
        try:
            self.vector_store = Chroma(
                persist_directory=settings.chroma_persist_dir,
                embedding_function=self.embeddings,
            )
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def load_and_index_documents(self, documents_path: str | None = None) -> None:
        """
        Load and index only NEW or MODIFIED documents (incremental indexing).
        
        Args:
            documents_path: Path to documents directory (uses settings default if None)
        """
        if documents_path is None:
            documents_path = str(settings.documents_dir)
        
        logger.info(f"Loading documents from {documents_path}")
        
        try:
            # Get all document files
            all_files = list(Path(documents_path).glob("*.txt"))
            if not all_files:
                logger.warning(f"No documents found in {documents_path}")
                return
            
            logger.info(f"Found {len(all_files)} total document files")
            
            # Load existing index metadata
            indexed_files = self._load_indexed_files()
            logger.info(f"Previously indexed: {len(indexed_files)} files")
            
            # Find new or modified files
            new_documents = []
            updated_metadata = indexed_files.copy()
            
            for file_path in all_files:
                file_str = str(file_path)
                current_hash = self._get_file_hash(file_str)
                
                # Check if file is new or modified
                if file_str not in indexed_files or indexed_files[file_str] != current_hash:
                    logger.info(f"New/modified file detected: {file_path.name}")
                    loader = TextLoader(file_str, encoding='utf-8')
                    docs = loader.load()
                    new_documents.extend(docs)
                    updated_metadata[file_str] = current_hash
            
            if not new_documents:
                logger.info("✓ No new or modified documents to index")
                return
            
            logger.info(f"Processing {len(new_documents)} new/modified documents")
            
            # Split new documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
            )
            splits = text_splitter.split_documents(new_documents)
            logger.info(f"Created {len(splits)} chunks from new documents")
            
            # Initialize vector store if needed
            if self.vector_store is None:
                self.initialize_vector_store()
            
            # Check if vector store is empty (first time indexing)
            try:
                # Try to get collection count
                collection = self.vector_store._collection
                existing_count = collection.count()
                is_empty = existing_count == 0
            except:
                is_empty = True
            
            if is_empty:
                # Create new vector store
                logger.info("Creating new vector store...")
                self.vector_store = Chroma.from_documents(
                    documents=splits,
                    embedding=self.embeddings,
                    persist_directory=settings.chroma_persist_dir,
                )
            else:
                # Add to existing vector store
                logger.info("Adding new documents to existing vector store...")
                self.vector_store.add_documents(splits)
            
            # Save updated metadata
            self._save_indexed_files(updated_metadata)
            logger.info(f"✓ Successfully indexed {len(new_documents)} new/modified documents")
            
        except Exception as e:
            logger.error(f"Failed to load and index documents: {e}")
            raise
    
    def retrieve(self, query: str, top_k: int | None = None) -> list[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve (uses settings default if None)
            
        Returns:
            List of relevant documents
        """
        if self.vector_store is None:
            self.initialize_vector_store()
        
        k = top_k or settings.retrieval_top_k
        
        logger.info(f"Retrieving top {k} documents for query: {query}")
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Retrieved {len(docs)} documents")
            return docs
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []
    
    def format_documents(self, docs: list[Document]) -> str:
        """
        Format retrieved documents into a context string.
        
        Args:
            docs: List of documents
            
        Returns:
            Formatted context string
        """
        if not docs:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            context_parts.append(f"[Document {i} - Source: {source}]\n{doc.page_content}")
        
        return "\n\n".join(context_parts)


# Global instance
_vector_store_manager: VectorStoreManager | None = None


def get_vector_store_manager() -> VectorStoreManager:
    """Get the global vector store manager instance."""
    global _vector_store_manager
    if _vector_store_manager is None:
        _vector_store_manager = VectorStoreManager()
    return _vector_store_manager

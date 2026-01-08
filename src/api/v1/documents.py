"""
Document management endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends

from src.api.dependencies import verify_api_key
from src.core import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/index", status_code=status.HTTP_200_OK)
async def index_documents(
    api_key: str = Depends(verify_api_key)
):
    """
    Index documents from the data/documents directory.
    
    Loads and indexes all documents into the vector store.
    """
    try:
        from src.retrieval.vector_store import get_vector_store_manager
        
        logger.info("Starting document indexing...")
        
        vsm = get_vector_store_manager()
        vsm.load_and_index_documents()
        
        logger.info("Document indexing completed")
        
        return {
            "status": "success",
            "message": "Documents indexed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error indexing documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index documents: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def documents_health():
    """Health check for document service."""
    return {
        "status": "healthy",
        "service": "documents"
    }

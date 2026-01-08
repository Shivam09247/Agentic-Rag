"""Source selection agent (Steps 5-6)."""

from src.core import SOURCE_TOOLS_API, SOURCE_VECTOR_DB, SOURCE_WEB_SEARCH, get_logger
from src.llms.model import get_agent_llm
from src.prompts.retrieval_prompt import SOURCE_SELECTION_PROMPT

logger = get_logger(__name__)


def select_source(query: str) -> str:
    """
    Select the best information source for the query.
    
    This agent chooses from:
    - vector_database: For document/knowledge base retrieval
    - tools_api: For external tools and APIs
    - web_search: For real-time internet information
    
    Args:
        query: The rewritten query
        
    Returns:
        The selected source name
    """
    logger.info(f"Selecting source for query: {query}")
    
    llm = get_agent_llm()
    chain = SOURCE_SELECTION_PROMPT | llm
    
    response = chain.invoke({"query": query})
    selected_source = response.content.strip().lower()
    
    # Validate and default to vector_database
    valid_sources = [SOURCE_VECTOR_DB, SOURCE_TOOLS_API, SOURCE_WEB_SEARCH]
    if selected_source not in valid_sources:
        logger.warning(f"Invalid source '{selected_source}', defaulting to vector_database")
        selected_source = SOURCE_VECTOR_DB
    
    logger.info(f"Selected source: {selected_source}")
    
    return selected_source

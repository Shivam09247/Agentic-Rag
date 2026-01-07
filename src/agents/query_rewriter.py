"""Query rewriting agent (Steps 1-2)."""

from src.llms.model import get_agent_llm
from src.prompts.rewrite_prompt import QUERY_REWRITE_PROMPT
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def rewrite_query(query: str) -> str:
    """
    Rewrite the user query for better retrieval.
    
    This agent:
    - Fixes spelling/grammar errors
    - Simplifies complex queries
    - Optimizes for semantic search
    
    Args:
        query: Original user query
        
    Returns:
        Rewritten query optimized for retrieval
    """
    logger.info(f"Rewriting query: {query}")
    
    llm = get_agent_llm()
    chain = QUERY_REWRITE_PROMPT | llm
    response = chain.invoke({"query": query})
    rewritten_query = response.content.strip()
    logger.info(f"Rewritten query: {rewritten_query}")
    
    return rewritten_query

"""Decision agent for determining if more information is needed (Steps 3-4)."""

from src.llms.model import get_agent_llm
from src.prompts.retrieval_prompt import NEEDS_MORE_INFO_PROMPT
from src.core import get_logger

logger = get_logger(__name__)


def check_needs_more_info(query: str) -> bool:
    """
    Determine if the query requires external information retrieval.
    
    This agent decides whether to:
    - Proceed with retrieval (returns True)
    - Answer directly without retrieval (returns False)
    
    Args:
        query: The rewritten query
        
    Returns:
        True if retrieval is needed, False otherwise
    """
    logger.info(f"Checking if query needs more info: {query}")
    
    llm = get_agent_llm()
    chain = NEEDS_MORE_INFO_PROMPT | llm
    response = chain.invoke({"query": query})
    decision = response.content.strip().upper()
    needs_info = decision == "YES"
    logger.info(f"Needs more info: {needs_info}")
    
    return needs_info

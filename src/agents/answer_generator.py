"""Answer generation agent (Steps 8-9)."""

from src.llms.model import get_generation_llm
from src.prompts.evaluation_prompt import (
    ANSWER_GENERATION_NO_CONTEXT_PROMPT,
    ANSWER_GENERATION_PROMPT,
)
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def generate_answer(query: str, context: str | None = None) -> str:
    """
    Generate an answer to the query using the provided context.
    
    This agent:
    - Uses context if available (retrieval path)
    - Generates directly if no context (direct answer path)
    
    Args:
        query: The user's query
        context: Retrieved context (optional)
        
    Returns:
        Generated answer
    """
    logger.info(f"Generating answer for query: {query}")
    logger.info(f"Context provided: {context is not None}")
    
    llm = get_generation_llm()
    
    if context:
        chain = ANSWER_GENERATION_PROMPT | llm
        response = chain.invoke({"query": query, "context": context})
    else:
        chain = ANSWER_GENERATION_NO_CONTEXT_PROMPT | llm
        response = chain.invoke({"query": query})
    
    answer = response.content.strip()
    
    logger.info(f"Generated answer: {answer[:100]}...")
    
    return answer

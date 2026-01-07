"""Answer evaluation agent (Steps 10-12)."""

from src.llms.model import get_agent_llm
from src.prompts.evaluation_prompt import ANSWER_EVALUATION_PROMPT
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def evaluate_answer(query: str, answer: str, context: str | None = None) -> bool:
    """
    Evaluate if the answer is relevant and satisfactory.
    
    This agent checks:
    - Answer relevance to the query
    - Consistency with context
    - Completeness and quality
    
    Args:
        query: The original query
        answer: The generated answer
        context: The context used (optional)
        
    Returns:
        True if answer is satisfactory, False if it needs improvement
    """
    logger.info(f"Evaluating answer for query: {query}")
    
    llm = get_agent_llm()
    chain = ANSWER_EVALUATION_PROMPT | llm
    
    context_str = context if context else "No context provided"
    
    response = chain.invoke({
        "query": query,
        "answer": answer,
        "context": context_str
    })
    
    decision = response.content.strip().upper()
    is_relevant = decision == "YES"
    
    logger.info(f"Answer is relevant: {is_relevant}")
    
    return is_relevant

"""LLM model configuration and initialization."""

from langchain_groq import ChatGroq
from src.core import settings, get_logger

logger = get_logger(__name__)

def get_llm(temperature: float | None = None, model: str | None = None) -> ChatGroq:
    """
    Get an initialized LLM instance.
    Args:
        temperature: Temperature for generation (uses settings.llm_temperature if not provided)
        model: Model name override (uses settings.llm_model if not provided)
        
    Returns:
        Configured ChatGroq instance
    """
    model_name = model or settings.llm_model
    temp = temperature if temperature is not None else settings.llm_temperature
    logger.info(f"Initializing LLM: {model_name} with temperature={temp}")
    
    return ChatGroq(
        model=model_name,
        temperature=temp,
        api_key=settings.groq_api_key,
    )

def get_agent_llm() -> ChatGroq:
    """Get LLM configured for agent reasoning tasks."""
    return get_llm(temperature=0.0)


def get_generation_llm() -> ChatGroq:
    """Get LLM configured for answer generation."""
    return get_llm(temperature=0.3)

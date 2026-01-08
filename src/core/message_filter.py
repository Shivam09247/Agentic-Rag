"""Message filtering utilities for context window management."""

from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from src.core import settings, get_logger

logger = get_logger(__name__)


def filter_messages_sliding_window(
    messages: List[BaseMessage], 
    max_messages: int = None
) -> List[BaseMessage]:
    """
    Apply sliding window to keep only recent messages.
    
    MongoDB stores ALL messages, but we only send recent ones to LLM.
    
    Args:
        messages: Full message history from MongoDB
        max_messages: Maximum messages to keep (uses settings if None)
        
    Returns:
        Filtered messages (most recent N messages)
    """
    if not messages:
        return messages
    
    if max_messages is None:
        max_messages = settings.max_context_messages
    
    if len(messages) <= max_messages:
        return messages
    
    # Keep only the last N messages (sliding window)
    filtered = messages[-max_messages:]
    
    logger.info(
        f"Filtered messages: {len(messages)} → {len(filtered)} "
        f"(sliding window: {max_messages})"
    )
    
    return filtered


def count_messages_by_type(messages: List[BaseMessage]) -> dict:
    """Count messages by type for debugging."""
    counts = {
        "human": 0,
        "ai": 0,
        "system": 0,
        "other": 0
    }
    
    for msg in messages:
        if isinstance(msg, HumanMessage):
            counts["human"] += 1
        elif isinstance(msg, AIMessage):
            counts["ai"] += 1
        elif isinstance(msg, SystemMessage):
            counts["system"] += 1
        else:
            counts["other"] += 1
    
    return counts


def get_conversation_summary(messages: List[BaseMessage]) -> str:
    """Get a summary of the conversation for logging."""
    if not messages:
        return "No messages"
    
    counts = count_messages_by_type(messages)
    return (
        f"Total: {len(messages)} messages "
        f"(Human: {counts['human']}, AI: {counts['ai']}, "
        f"System: {counts['system']})"
    )

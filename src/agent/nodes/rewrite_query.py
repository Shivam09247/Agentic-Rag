"""
Rewrite Query Node - Improves user queries for better retrieval
"""
from typing import Dict, Any

from ..state import AgentState
from ...llm.client import get_llm
from ...prompts.rewrite import QUERY_REWRITE_PROMPT, CONTEXTUAL_REWRITE_PROMPT
from ...config.logging import get_logger

logger = get_logger("agent.nodes.rewrite_query")


def rewrite_query_node(state: AgentState) -> Dict[str, Any]:
    """
    Rewrite the user query for better retrieval results.
    This node:
    1. Analyzes the original query
    2. Fixes spelling/grammar
    3. Expands abbreviations
    4. Makes implicit questions explicit
    5. Considers conversation context if available
    """
    logger.info("Rewriting query...")
    query = state.get("query", "")
    messages = state.get("messages", [])
    # Build conversation context if available
    conversation_context = ""
    if len(messages) > 1:
        recent_messages = messages[-5:]  # Last 5 messages
        context_parts = []
        for msg in recent_messages[:-1]:  # Exclude current query
            role = msg.get("role", "user")
            content = msg.get("content", "")
            context_parts.append(f"{role}: {content}")
        
        if context_parts:
            conversation_context = f"Conversation context:\n" + "\n".join(context_parts)
    try:
        llm = get_llm(temperature=0.3)  # Lower temperature for more focused rewriting
        
        # Use contextual rewrite if we have conversation history
        if conversation_context:
            prompt = CONTEXTUAL_REWRITE_PROMPT.format(
                history=conversation_context,
                query=query
            )
        else:
            prompt = QUERY_REWRITE_PROMPT.format(
                query=query,
                conversation_context=conversation_context
            )
        rewritten = llm.invoke(prompt).strip()
        # Clean up the response
        rewritten = rewritten.replace("Rewritten Query:", "").strip()
        rewritten = rewritten.strip('"').strip("'")
        # If rewrite is empty or too different, keep original
        if not rewritten or len(rewritten) > len(query) * 3:
            rewritten = query
        logger.info(f"Query rewritten: '{query[:50]}...' -> '{rewritten[:50]}...'")
        return {
            "rewritten_query": rewritten,
            "iteration": state.get("iteration", 0) + 1
        }
    except Exception as e:
        logger.error(f"Query rewrite failed: {e}")
        # Fall back to original query
        return {
            "rewritten_query": query,
            "iteration": state.get("iteration", 0) + 1
        }

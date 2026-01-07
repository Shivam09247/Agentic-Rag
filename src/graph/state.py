"""Shared state definition for the Agentic RAG graph."""

from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgenticRAGState(TypedDict):
    """
    State for the Agentic RAG workflow.
    
    This state is shared across all nodes in the graph and tracks:
    - User query and its rewritten version
    - Whether retrieval is needed
    - Selected source and retrieved context
    - Generated answer and evaluation results
    - Iteration tracking for retry logic
    """
    original_query: str
    rewritten_query: str
    needs_retrieval: bool
    selected_source: str
    retrieved_context: str
    answer: str
    answer_is_relevant: bool
    iteration: int
    max_iterations: int
    error: str | None
    messages: Annotated[list, add_messages]

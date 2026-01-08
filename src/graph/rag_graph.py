"""LangGraph workflow for Agentic RAG."""

from typing import Literal, Optional, Dict, Any

from langgraph.graph import END, START, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.agents.answer_evaluator import evaluate_answer
from src.agents.answer_generator import generate_answer
from src.agents.needs_more_info import check_needs_more_info
from src.agents.query_rewriter import rewrite_query
from src.agents.source_selector import select_source
from src.core import (
    settings,
    get_logger,
    SOURCE_TOOLS_API,
    SOURCE_VECTOR_DB,
    SOURCE_WEB_SEARCH,
)
from src.retrieval.tools import get_tools_manager
from src.retrieval.vector_store import get_vector_store_manager
from src.retrieval.web_search import get_web_search_manager
from src.graph.state import AgenticRAGState
from src.memory.database import get_database_service
from src.core.message_filter import filter_messages_sliding_window, get_conversation_summary

logger = get_logger(__name__)


# Node Functions
def query_rewriter_node(state: AgenticRAGState) -> dict:
    """Step 1-2: Rewrite the user query."""
    logger.info("=== Query Rewriter Node ===")
    
    rewritten = rewrite_query(state["original_query"])
    
    # Add system message about query rewriting
    system_msg = SystemMessage(content=f"Query rewritten to: {rewritten}")
    
    return {
        "rewritten_query": rewritten,
        "messages": [system_msg],
    }


def needs_more_info_node(state: AgenticRAGState) -> dict:
    """Step 3: Decide if more information is needed."""
    logger.info("=== Needs More Info Node ===")
    
    needs_info = check_needs_more_info(state["rewritten_query"])
    
    return {
        "needs_retrieval": needs_info,
        "messages": [f"Needs retrieval: {needs_info}"],
    }


def source_selector_node(state: AgenticRAGState) -> dict:
    """Step 5-6: Select the best information source."""
    logger.info("=== Source Selector Node ===")
    
    source = select_source(state["rewritten_query"])
    
    return {
        "selected_source": source,
        "messages": [f"Selected source: {source}"],
    }


def retriever_node(state: AgenticRAGState) -> dict:
    """Step 7: Retrieve information from the selected source."""
    logger.info("=== Retriever Node ===")
    
    query = state["rewritten_query"]
    source = state["selected_source"]
    context = ""
    
    try:
        if source == SOURCE_VECTOR_DB:
            # Vector database retrieval
            vsm = get_vector_store_manager()
            docs = vsm.retrieve(query)
            context = vsm.format_documents(docs)
            
        elif source == SOURCE_TOOLS_API:
            # Tools/API retrieval
            tm = get_tools_manager()
            context = tm.get_tools_info()
            # In a real implementation, you'd parse the query and execute relevant tools
            
        elif source == SOURCE_WEB_SEARCH:
            # Web search retrieval
            wsm = get_web_search_manager()
            context = wsm.search(query)
        
        logger.info(f"Retrieved context length: {len(context)}")
        
    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        context = f"Error during retrieval: {str(e)}"
    
    return {
        "retrieved_context": context,
        "messages": [f"Retrieved context from {source}"],
    }


def answer_generator_node(state: AgenticRAGState) -> dict:
    """Step 8-9: Generate answer with sliding window context management."""
    logger.info("=== Answer Generator Node ===")
    
    query = state["rewritten_query"]
    context = state.get("retrieved_context")
    
    # Get full message history from state (MongoDB stores all)
    all_messages = state.get("messages", [])
    logger.info(f"Full conversation: {get_conversation_summary(all_messages)}")
    
    # Apply sliding window: Only use recent messages for LLM context
    # MongoDB keeps all messages, but we only send last N to the model
    filtered_messages = filter_messages_sliding_window(all_messages)
    logger.info(f"Filtered for LLM: {len(filtered_messages)} messages")
    
    # TODO: Use filtered_messages when calling LLM with conversation history
    # For now, generate_answer doesn't use message history yet
    answer = generate_answer(query, context)
    
    # Add AI response message (will be stored in MongoDB)
    ai_msg = AIMessage(content=answer)
    
    return {
        "answer": answer,
        "messages": [ai_msg],  # MongoDB stores this with all previous messages
    }


def answer_evaluator_node(state: AgenticRAGState) -> dict:
    """Step 10: Evaluate answer quality."""
    logger.info("=== Answer Evaluator Node ===")
    
    query = state["rewritten_query"]
    answer = state["answer"]
    context = state.get("retrieved_context")
    
    is_relevant = evaluate_answer(query, answer, context)
    
    # Increment iteration counter
    current_iteration = state.get("iteration", 0) + 1
    
    return {
        "answer_is_relevant": is_relevant,
        "iteration": current_iteration,
        "messages": [f"Answer is relevant: {is_relevant} (Iteration: {current_iteration})"],
    }


# Conditional Edges
def route_after_needs_info(
    state: AgenticRAGState,
) -> Literal["source_selector", "answer_generator"]:
    """Route based on whether retrieval is needed."""
    if state["needs_retrieval"]:
        return "source_selector"
    else:
        return "answer_generator"


def route_after_evaluation(
    state: AgenticRAGState,
) -> Literal["query_rewriter", "end"]:
    """Route based on answer quality and iteration count."""
    is_relevant = state.get("answer_is_relevant", False)
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", settings.max_iterations)
    
    # If answer is relevant or max iterations reached, end
    if is_relevant:
        logger.info("Answer is relevant, ending workflow")
        return "end"
    
    if iteration >= max_iterations:
        logger.info(f"Max iterations ({max_iterations}) reached, ending workflow")
        return "end"
    
    # Otherwise, retry from the beginning
    logger.info("Answer not relevant, retrying...")
    return "query_rewriter"


# Build the Graph
def create_agentic_rag_graph(checkpointer=None) -> StateGraph:
    """
    Create the Agentic RAG workflow graph.
    
    Args:
        checkpointer: Optional checkpointer for persistence (uses MongoDB by default)
    
    Returns:
        Compiled LangGraph workflow with memory
    """
    logger.info("Creating Agentic RAG graph...")
    
    # Initialize graph
    workflow = StateGraph(AgenticRAGState)
    
    # Add nodes
    workflow.add_node("query_rewriter", query_rewriter_node)
    workflow.add_node("needs_more_info", needs_more_info_node)
    workflow.add_node("source_selector", source_selector_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("answer_generator", answer_generator_node)
    workflow.add_node("answer_evaluator", answer_evaluator_node)
    
    # Add edges
    workflow.add_edge(START, "query_rewriter")
    workflow.add_edge("query_rewriter", "needs_more_info")
    
    # Conditional edge: needs info?
    workflow.add_conditional_edges(
        "needs_more_info",
        route_after_needs_info,
        {
            "source_selector": "source_selector",
            "answer_generator": "answer_generator",
        },
    )
    
    # Retrieval path
    workflow.add_edge("source_selector", "retriever")
    workflow.add_edge("retriever", "answer_generator")
    
    # Evaluation path
    workflow.add_edge("answer_generator", "answer_evaluator")
    
    # Conditional edge: answer relevant?
    workflow.add_conditional_edges(
        "answer_evaluator",
        route_after_evaluation,
        {
            "query_rewriter": "query_rewriter",  # Retry
            "end": END,  # Success or max iterations
        },
    )
    
    # MongoDB checkpointer for persistent session memory (stores ALL messages)
    # Uses DatabaseService singleton pattern for connection management
    if checkpointer is None:
        db_service = get_database_service()  # Singleton instance
        checkpointer = db_service.get_checkpointer()  # Get MongoDB checkpointer
        logger.info("Using MongoDB checkpointer for session persistence")
    
    # Compile graph with checkpointer for memory persistence
    # This enables: thread-based conversations, state persistence, message history
    app = workflow.compile(checkpointer=checkpointer)
    
    logger.info("Agentic RAG graph created successfully with memory persistence")
    
    return app


def run_agentic_rag(query: str, thread_id: str) -> Dict[str, Any]:
    """
    Run the agentic RAG workflow for a given query.
    
    Args:
        query: User query to process
        thread_id: Thread ID for session persistence
        
    Returns:
        Dictionary containing the answer and metadata
    """
    # Create graph with MongoDB checkpointer
    graph = create_agentic_rag_graph()
    
    # Initial state
    initial_state = {
        "original_query": query,
        "rewritten_query": "",
        "needs_retrieval": False,
        "selected_source": None,
        "retrieved_context": "",
        "answer": "",
        "answer_is_relevant": False,
        "iteration": 0,
        "messages": [HumanMessage(content=query)],
    }
    
    # Configuration with thread_id for session persistence
    config = {"configurable": {"thread_id": thread_id}}
    
    # Run graph
    result = graph.invoke(initial_state, config)
    
    logger.info(f"RAG workflow completed for thread {thread_id[:16]}...")
    
    return result


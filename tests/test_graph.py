"""Tests for Agentic RAG graph workflow."""

import pytest

from src.graph.rag_graph import create_agentic_rag_graph, run_agentic_rag
from src.graph.state import AgenticRAGState


class TestRAGGraph:
    """Tests for the RAG graph workflow."""
    
    def test_create_graph(self):
        """Test that graph can be created."""
        graph = create_agentic_rag_graph()
        assert graph is not None
    
    def test_simple_query(self):
        """Test processing a simple query."""
        result = run_agentic_rag("What is 2 + 2?")
        
        assert isinstance(result, dict)
        assert "answer" in result
        assert "original_query" in result
        assert result["original_query"] == "What is 2 + 2?"
        assert len(result["answer"]) > 0
    
    def test_query_with_retrieval(self):
        """Test processing a query that may need retrieval."""
        result = run_agentic_rag("Explain machine learning")
        
        assert isinstance(result, dict)
        assert "answer" in result
        assert "needs_retrieval" in result
        assert len(result["answer"]) > 0
    
    def test_state_structure(self):
        """Test that state has correct structure."""
        result = run_agentic_rag("Test query")
        
        # Check required state fields
        assert "original_query" in result
        assert "rewritten_query" in result
        assert "needs_retrieval" in result
        assert "answer" in result
        assert "answer_is_relevant" in result
        assert "iteration" in result

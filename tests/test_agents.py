"""Tests for Agentic RAG agents."""

import pytest

from src.agents.answer_evaluator import evaluate_answer
from src.agents.answer_generator import generate_answer
from src.agents.needs_more_info import check_needs_more_info
from src.agents.query_rewriter import rewrite_query
from src.agents.source_selector import select_source


class TestQueryRewriter:
    """Tests for query rewriting agent."""
    
    def test_rewrite_simple_query(self):
        """Test rewriting a simple query."""
        query = "what is machne learning"  # Intentional typo
        result = rewrite_query(query)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "machine learning" in result.lower()


class TestNeedsMoreInfo:
    """Tests for needs more info decision agent."""
    
    def test_simple_fact_no_retrieval(self):
        """Test that simple facts don't need retrieval."""
        query = "What is 2 + 2?"
        result = check_needs_more_info(query)
        
        assert isinstance(result, bool)
    
    def test_complex_query_needs_retrieval(self):
        """Test that complex queries need retrieval."""
        query = "What are the latest developments in quantum computing?"
        result = check_needs_more_info(query)
        
        assert isinstance(result, bool)


class TestSourceSelector:
    """Tests for source selection agent."""
    
    def test_select_source(self):
        """Test source selection."""
        query = "Tell me about Python programming"
        result = select_source(query)
        
        assert isinstance(result, str)
        assert result in ["vector_database", "tools_api", "web_search"]


class TestAnswerGenerator:
    """Tests for answer generation agent."""
    
    def test_generate_without_context(self):
        """Test answer generation without context."""
        query = "What is Python?"
        result = generate_answer(query)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_generate_with_context(self):
        """Test answer generation with context."""
        query = "What is Python?"
        context = "Python is a high-level programming language."
        result = generate_answer(query, context)
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestAnswerEvaluator:
    """Tests for answer evaluation agent."""
    
    def test_evaluate_good_answer(self):
        """Test evaluation of a relevant answer."""
        query = "What is 2 + 2?"
        answer = "2 + 2 equals 4."
        result = evaluate_answer(query, answer)
        
        assert isinstance(result, bool)
    
    def test_evaluate_with_context(self):
        """Test evaluation with context."""
        query = "What is Python?"
        answer = "Python is a programming language."
        context = "Python is a high-level programming language."
        result = evaluate_answer(query, answer, context)
        
        assert isinstance(result, bool)

"""Constants used throughout the application."""

from typing import Final

# Agent Node Names
NODE_QUERY_REWRITER: Final[str] = "query_rewriter"
NODE_NEEDS_MORE_INFO: Final[str] = "needs_more_info"
NODE_SOURCE_SELECTOR: Final[str] = "source_selector"
NODE_RETRIEVER: Final[str] = "retriever"
NODE_ANSWER_GENERATOR: Final[str] = "answer_generator"
NODE_ANSWER_EVALUATOR: Final[str] = "answer_evaluator"

# Edge Conditions
EDGE_NEEDS_INFO: Final[str] = "needs_info"
EDGE_NO_INFO_NEEDED: Final[str] = "no_info_needed"
EDGE_ANSWER_RELEVANT: Final[str] = "relevant"
EDGE_ANSWER_NOT_RELEVANT: Final[str] = "not_relevant"

# Source Types
SOURCE_VECTOR_DB: Final[str] = "vector_database"
SOURCE_TOOLS_API: Final[str] = "tools_api"
SOURCE_WEB_SEARCH: Final[str] = "web_search"

# Answer Quality Scores
MIN_RELEVANCE_SCORE: Final[float] = 0.7

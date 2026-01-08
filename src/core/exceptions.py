"""Custom exceptions for Agentic RAG system."""


class ConfigurationError(Exception):
    """Raised when there's a configuration error."""
    pass


class DatabaseError(Exception):
    """Raised when there's a database error."""
    pass


class RetrievalError(Exception):
    """Raised when there's a retrieval error."""
    pass


class LLMError(Exception):
    """Raised when there's an LLM error."""
    pass

"""Web search integration for real-time information retrieval."""

from typing import Any

from src.config.settings import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class WebSearchManager:
    """Manages web search operations."""
    
    def __init__(self):
        """Initialize web search manager."""
        self.search_provider: str | None = None
        self._initialize_search_provider()
    
    def _initialize_search_provider(self) -> None:
        """Initialize the search provider based on available API keys."""
        if settings.tavily_api_key:
            self.search_provider = "tavily"
            logger.info("Using Tavily for web search")
        elif settings.serpapi_api_key:
            self.search_provider = "serpapi"
            logger.info("Using SerpAPI for web search")
        else:
            self.search_provider = None
            logger.warning("No web search provider configured")
    
    def search(self, query: str, max_results: int = 5) -> str:
        """
        Perform a web search.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted search results
        """
        logger.info(f"Performing web search: {query}")
        
        if self.search_provider is None:
            return self._mock_search(query)
        
        if self.search_provider == "tavily":
            return self._tavily_search(query, max_results)
        elif self.search_provider == "serpapi":
            return self._serpapi_search(query, max_results)
        else:
            return self._mock_search(query)
    
    def _tavily_search(self, query: str, max_results: int) -> str:
        """
        Search using Tavily API.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            Search results
        """
        try:
            import os
            from langchain_community.tools.tavily_search import TavilySearchResults
            
            # Set environment variable for Tavily
            os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
            
            tool = TavilySearchResults(
                max_results=max_results,
            )
            
            results = tool.invoke({"query": query})
            return self._format_search_results(results)
            
        except ImportError:
            logger.warning("Tavily not installed, using mock search")
            return self._mock_search(query)
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return f"Web search error: {str(e)}"
    
    def _serpapi_search(self, query: str, max_results: int) -> str:
        """
        Search using SerpAPI.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            Search results
        """
        try:
            from langchain_community.utilities import SerpAPIWrapper
            
            search = SerpAPIWrapper(serpapi_api_key=settings.serpapi_api_key)
            results = search.run(query)
            
            return f"Web Search Results:\n{results}"
            
        except ImportError:
            logger.warning("SerpAPI not installed, using mock search")
            return self._mock_search(query)
        except Exception as e:
            logger.error(f"SerpAPI search failed: {e}")
            return f"Web search error: {str(e)}"
    
    def _mock_search(self, query: str) -> str:
        """
        Mock search for when no provider is configured.
        
        Args:
            query: Search query
            
        Returns:
            Mock results message
        """
        logger.info("Using mock web search")
        return (
            f"[Mock Web Search Results for: {query}]\n\n"
            "Note: No web search provider configured. "
            "Set TAVILY_API_KEY or SERPAPI_API_KEY in .env to enable real web search.\n\n"
            "This is a placeholder for web search results."
        )
    
    def _format_search_results(self, results: list[dict[str, Any]]) -> str:
        """
        Format search results into a readable string.
        
        Args:
            results: Raw search results
            
        Returns:
            Formatted results
        """
        if not results:
            return "No web search results found."
        
        formatted = ["Web Search Results:\n"]
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            content = result.get("content", result.get("snippet", "No content"))
            url = result.get("url", "")
            
            formatted.append(f"[Result {i}]")
            formatted.append(f"Title: {title}")
            formatted.append(f"Content: {content}")
            if url:
                formatted.append(f"URL: {url}")
            formatted.append("")
        
        return "\n".join(formatted)


# Global instance
_web_search_manager: WebSearchManager | None = None


def get_web_search_manager() -> WebSearchManager:
    """Get the global web search manager instance."""
    global _web_search_manager
    if _web_search_manager is None:
        _web_search_manager = WebSearchManager()
    return _web_search_manager

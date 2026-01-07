"""External tools and APIs integration."""

from typing import Any

from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class ToolsManager:
    """Manages external tools and API integrations."""
    
    def __init__(self):
        """Initialize tools manager."""
        self.available_tools: dict[str, Any] = {}
        self._register_default_tools()
    
    def _register_default_tools(self) -> None:
        """Register default tools available to the system."""
        # Example: Calculator tool
        self.available_tools["calculator"] = self._calculator_tool
        
        # Example: Date/time tool
        self.available_tools["datetime"] = self._datetime_tool
        
        logger.info(f"Registered {len(self.available_tools)} tools")
    
    def _calculator_tool(self, expression: str) -> str:
        """
        Simple calculator tool.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Result as string
        """
        try:
            # Safe evaluation (basic expressions only)
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _datetime_tool(self, query: str) -> str:
        """
        Date/time information tool.
        
        Args:
            query: Date/time query
            
        Returns:
            Date/time information
        """
        from datetime import datetime
        
        now = datetime.now()
        return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def execute_tool(self, tool_name: str, **kwargs: Any) -> str:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool-specific arguments
            
        Returns:
            Tool execution result
        """
        logger.info(f"Executing tool: {tool_name}")
        
        if tool_name not in self.available_tools:
            logger.warning(f"Tool '{tool_name}' not found")
            return f"Tool '{tool_name}' is not available."
        
        try:
            result = self.available_tools[tool_name](**kwargs)
            logger.info(f"Tool execution successful: {tool_name}")
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"Error executing tool: {str(e)}"
    
    def get_tools_info(self) -> str:
        """
        Get information about available tools.
        
        Returns:
            Description of available tools
        """
        return f"Available tools: {', '.join(self.available_tools.keys())}"


# Global instance
_tools_manager: ToolsManager | None = None


def get_tools_manager() -> ToolsManager:
    """Get the global tools manager instance."""
    global _tools_manager
    if _tools_manager is None:
        _tools_manager = ToolsManager()
    return _tools_manager

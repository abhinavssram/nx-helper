# tool_executor.py
from typing import Dict, Any, List
from langchain_core.tools import Tool

class ToolExecutor:
    """Executes tools based on LLM output"""
    
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a specific tool with given arguments"""
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
        
        try:
            tool = self.tools[tool_name]
            result = tool.func(**kwargs)
            return result
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.tools.keys())
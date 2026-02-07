"""MCP server implementation using Official MCP SDK."""

from typing import Dict, Any, Callable
from sqlmodel import Session
from .tools.task_tools import (
    AddTaskTool, ListTasksTool, CompleteTaskTool, UpdateTaskTool, DeleteTaskTool
)
from ...database import engine


class MCPServer:
    """
    MCP server that manages task management tools for AI agent execution.
    This server follows stateless architecture principles and delegates
    execution to specialized tools while maintaining no in-memory state.
    """

    def __init__(self):
        """Initialize the MCP server with available tools."""
        self.tools = {
            'add_task': self._execute_add_task,
            'list_tasks': self._execute_list_tasks,
            'complete_task': self._execute_complete_task,
            'update_task': self._execute_update_task,
            'delete_task': self._execute_delete_task
        }

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool with the given parameters.

        Args:
            tool_name: Name of the tool to execute
            params: Parameters to pass to the tool

        Returns:
            Result of the tool execution with success/error information
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "INVALID_TOOL",
                    "message": f"Tool '{tool_name}' is not available",
                    "details": {"requested_tool": tool_name}
                }
            }

        # Create a new database session for this request (stateless)
        with Session(engine) as db_session:
            # Execute the requested tool
            return self.tools[tool_name](params, db_session)

    def _execute_add_task(self, params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
        """Execute the add_task tool."""
        tool = AddTaskTool(db_session)
        return tool.run(params)

    def _execute_list_tasks(self, params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
        """Execute the list_tasks tool."""
        tool = ListTasksTool(db_session)
        return tool.run(params)

    def _execute_complete_task(self, params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
        """Execute the complete_task tool."""
        tool = CompleteTaskTool(db_session)
        return tool.run(params)

    def _execute_update_task(self, params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
        """Execute the update_task tool."""
        tool = UpdateTaskTool(db_session)
        return tool.run(params)

    def _execute_delete_task(self, params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
        """Execute the delete_task tool."""
        tool = DeleteTaskTool(db_session)
        return tool.run(params)

    def get_available_tools(self) -> list:
        """Get list of available tools."""
        return list(self.tools.keys())


# Singleton instance of the MCP server
mcp_server = MCPServer()


def get_mcp_server() -> MCPServer:
    """Get the singleton instance of the MCP server."""
    return mcp_server
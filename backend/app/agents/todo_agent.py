from openai import OpenAI
from typing import Dict, Any, List, Optional
import os
from ..mcp_tools.todo_mcp_tools import TodoMCPTasks
from sqlmodel import Session
from ..database import engine


class TodoAgent:
    """
    AI agent that handles natural language processing for todo management.
    Uses OpenAI's API to interpret user requests and delegate to MCP tools.
    """

    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)

        # System instructions for the agent
        self.system_prompt = """
        You are a helpful todo management assistant. Your job is to interpret user requests about managing tasks and translate them into appropriate actions using the provided tools.

        When a user asks to:
        - Add/create/remember a task: Use the add_task tool
        - View/list/show tasks: Use the list_tasks tool
        - Mark/complete/finish a task: Use the complete_task tool
        - Remove/delete a task: Use the delete_task tool
        - Change/update/edit a task: Use the update_task tool

        Always ask for clarification if the user's request is ambiguous.
        Respond in a friendly, helpful tone.
        """

    def run_conversation(self,
                       messages: List[Dict[str, str]],
                       user_id: int,
                       tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Run a conversation with the AI agent, including tool calls.

        Args:
            messages: List of conversation messages [{"role": "...", "content": "..."}]
            user_id: ID of the user interacting with the agent
            tools: List of available tools (will be populated with MCP tools if not provided)

        Returns:
            Dict containing the assistant response and any tool call results
        """
        # Create database session for MCP tools
        db_session = Session(engine)

        try:
            # Initialize MCP tools with the session
            mcp_tools = TodoMCPTasks(db_session)

            # Define available tools if not provided
            if tools is None:
                tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": "add_task",
                            "description": "Create a new todo task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "Title of the task"},
                                    "description": {"type": "string", "description": "Optional description of the task"}
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "list_tasks",
                            "description": "Retrieve user's todo tasks",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "completed": {
                                        "type": "boolean",
                                        "description": "Filter by completion status (true for completed, false for incomplete, null for all)"
                                    }
                                },
                                "required": []
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "complete_task",
                            "description": "Mark a task as completed or uncompleted",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "integer", "description": "ID of the task to update"},
                                    "completed": {"type": "boolean", "description": "Whether the task is completed (default: true)"}
                                },
                                "required": ["task_id"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "delete_task",
                            "description": "Remove a todo task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "integer", "description": "ID of the task to delete"}
                                },
                                "required": ["task_id"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "update_task",
                            "description": "Modify an existing todo task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "integer", "description": "ID of the task to update"},
                                    "title": {"type": "string", "description": "New title for the task (optional)"},
                                    "description": {"type": "string", "description": "New description for the task (optional)"},
                                    "completed": {"type": "boolean", "description": "New completion status for the task (optional)"}
                                },
                                "required": ["task_id"]
                            }
                        }
                    }
                ]

            # Add the system message to the beginning if it's not already there
            if not messages or messages[0]["role"] != "system":
                messages = [{"role": "system", "content": self.system_prompt}] + messages

            # Call the OpenAI API with the messages and tools
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # Get the response message
            response_message = response.choices[0].message

            # Initialize result
            result = {
                "response": response_message.content or "",
                "tool_calls": [],
                "tool_results": []
            }

            # Process tool calls if any
            if response_message.tool_calls:
                import json
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add user_id to function arguments since all tools require it
                    function_args["user_id"] = user_id

                    # Call the appropriate tool function
                    tool_result = None
                    if hasattr(mcp_tools, function_name):
                        tool_method = getattr(mcp_tools, function_name)
                        tool_result = tool_method(**function_args)
                    else:
                        tool_result = {
                            "success": False,
                            "data": None,
                            "error": {
                                "code": "UNKNOWN_TOOL",
                                "message": f"Unknown tool: {function_name}",
                                "details": {"tool_name": function_name}
                            }
                        }

                    # Store the tool call and its result
                    result["tool_calls"].append({
                        "name": function_name,
                        "arguments": function_args,
                        "id": tool_call.id
                    })
                    result["tool_results"].append(tool_result)

            return result

        finally:
            # Close the database session
            db_session.close()
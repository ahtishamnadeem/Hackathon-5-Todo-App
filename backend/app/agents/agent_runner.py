"""Agent runner for processing chat requests with multi-provider fallback."""

import logging
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from sqlmodel import Session, select
from openai import OpenAI
import google.generativeai as genai
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.user import User
from ..mcp_tools.todo_mcp_tools import TodoMCPTasks
from ..database import engine
from .task_command_parser import TaskCommandParser

# Set up logging for observability and traceability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseMCPTaskTool(ABC):
    """Base class for MCP task tools with common functionality."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def validate_user_exists(self, user_id: int) -> bool:
        """Verify that the user exists in the database."""
        user = self.db.get(User, user_id)
        return user is not None

    def validate_task_ownership(self, task_id: int, user_id: int) -> bool:
        """Verify that the task belongs to the specified user."""
        from ..models.todo import Todo
        task = self.db.get(Todo, task_id)
        if not task:
            return False
        return task.user_id == user_id

    def format_success_response(self, data: Any) -> Dict[str, Any]:
        """Format a successful response following MCP contract."""
        return {
            "success": True,
            "data": data,
            "error": None
        }

    def format_error_response(self, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format an error response following MCP contract."""
        return {
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message,
                "details": details or {}
            }
        }


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def call_ai(self, messages: List[Dict[str, str]], tools: List[Dict]) -> Tuple[str, List[Dict], bool]:
        """
        Call the AI provider.

        Returns:
            Tuple of (response_text, tool_calls, quota_exceeded)
        """
        pass


class OpenAIProvider(AIProvider):
    """OpenAI provider implementation."""

    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def call_ai(self, messages: List[Dict[str, str]], tools: List[Dict]) -> Tuple[str, List[Dict], bool]:
        """Call OpenAI API with tool support."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            content = response_message.content or ""

            # Convert OpenAI tool calls to standard format
            tool_calls = []
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_calls.append({
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })

            return content, tool_calls, False

        except Exception as e:
            error_str = str(e)
            # Check for quota/rate limit errors
            if "429" in error_str or "quota" in error_str.lower() or "rate_limit" in error_str.lower():
                logger.warning(f"OpenAI quota exceeded: {error_str}")
                return "", [], True
            raise


class GoogleAIProvider(AIProvider):
    """Google AI (Gemini) provider implementation."""

    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model_name = model

    def call_ai(self, messages: List[Dict[str, str]], tools: List[Dict]) -> Tuple[str, List[Dict], bool]:
        """Call Google AI API with tool support and retry logic."""
        import time

        max_retries = 3
        base_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Extract system instruction and user message
                system_instruction = ""
                user_message = ""

                for msg in messages:
                    if msg["role"] == "system":
                        system_instruction = msg["content"]
                    elif msg["role"] == "user":
                        user_message = msg["content"]  # Get last user message

                if not user_message:
                    logger.error("No user message found in conversation")
                    raise ValueError("No user message found")

                logger.info(f"Generating content with model: {self.model_name} (attempt {attempt + 1}/{max_retries})")

                # Convert OpenAI tools to Gemini function declarations
                gemini_tools = None
                if tools:
                    try:
                        function_declarations = []
                        for tool in tools:
                            func = tool["function"]
                            function_declarations.append(
                                genai.protos.FunctionDeclaration(
                                    name=func["name"],
                                    description=func["description"],
                                    parameters=genai.protos.Schema(
                                        type=genai.protos.Type.OBJECT,
                                        properties={
                                            prop_name: genai.protos.Schema(
                                                type=genai.protos.Type.STRING if prop_def.get("type") == "string"
                                                else genai.protos.Type.INTEGER if prop_def.get("type") == "integer"
                                                else genai.protos.Type.OBJECT,
                                                description=prop_def.get("description", "")
                                            )
                                            for prop_name, prop_def in func["parameters"].get("properties", {}).items()
                                        },
                                        required=func["parameters"].get("required", [])
                                    )
                                )
                            )

                        gemini_tools = [genai.protos.Tool(function_declarations=function_declarations)]
                        logger.info(f"Converted {len(function_declarations)} tools for Gemini")
                    except Exception as e:
                        logger.warning(f"Failed to convert tools, proceeding without them: {e}")
                        gemini_tools = None

                # Create model with system instruction
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction if system_instruction else None,
                    tools=gemini_tools
                )

                # Generate response
                response = model.generate_content(user_message)

                # Extract text content
                content = ""
                if hasattr(response, 'text'):
                    try:
                        content = response.text
                        logger.info(f"Got response from Google AI: {content[:100]}...")
                    except ValueError as ve:
                        # Text might not be available if only function calls were made
                        logger.info(f"No text in response (might have function calls): {ve}")
                        content = ""

                # Extract tool calls if any
                tool_calls = []
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call'):
                                fc = part.function_call
                                # Convert Gemini function call to standard format
                                args = {}
                                for key, value in fc.args.items():
                                    args[key] = value

                                tool_calls.append({
                                    "name": fc.name,
                                    "arguments": args
                                })
                                logger.info(f"Function call detected: {fc.name}")

                return content, tool_calls, False

            except Exception as e:
                error_str = str(e)
                logger.error(f"Google AI error (attempt {attempt + 1}/{max_retries}): {type(e).__name__}: {error_str}")

                # Check for rate limit errors
                is_rate_limit = any(keyword in error_str.lower() for keyword in ["rate", "quota", "429", "resource_exhausted"])

                if is_rate_limit and attempt < max_retries - 1:
                    # Exponential backoff
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Rate limit hit, waiting {delay} seconds before retry...")
                    time.sleep(delay)
                    continue
                elif is_rate_limit:
                    # All retries exhausted
                    logger.warning(f"Google AI quota exceeded after {max_retries} attempts")
                    return "", [], True
                else:
                    # Non-rate-limit error, raise it
                    raise

        # Should not reach here, but just in case
        return "", [], True


class AgentRunner:
    """
    Orchestrates the execution of the AI agent with multi-provider fallback,
    managing conversation state, message persistence, and tool integration.
    """

    def __init__(self):
        """Initialize the agent runner with multiple AI providers and local task parser."""
        self.tools = TodoMCPTasks()
        self.task_parser = TaskCommandParser()  # Local command parser for instant responses

        # Initialize providers
        self.providers = []

        # Try to initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                self.providers.append(("OpenAI", OpenAIProvider(
                    openai_key,
                    os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                )))
                logger.info("OpenAI provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")

        # Try to initialize Google AI
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            try:
                self.providers.append(("Google AI", GoogleAIProvider(
                    google_key,
                    os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")
                )))
                logger.info("Google AI provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google AI: {e}")

        if not self.providers:
            raise ValueError("No AI providers available. Please configure OPENAI_API_KEY or GOOGLE_API_KEY")

        # Define the tools available to the agent (OpenAI format, will be converted for other providers)
        self.available_tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new todo task for the user",
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
                    "description": "Retrieve the user's todo tasks with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter tasks by completion status"
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
                    "description": "Mark a specific task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "ID of the task to complete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify an existing task's title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task (optional)"},
                            "description": {"type": "string", "description": "New description for the task (optional)"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a specific task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "ID of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

        # System prompt for the AI agent
        self.system_prompt = {
            "role": "system",
            "content": """You are an intelligent AI assistant specialized in helping users manage their todo tasks efficiently.

## YOUR ROLE AND PERSONALITY
- You are friendly, helpful, and proactive
- You communicate clearly and concisely
- You always confirm actions you take
- You provide helpful suggestions when appropriate
- You celebrate user accomplishments

## YOUR CAPABILITIES
You have access to the following tools to manage tasks:

1. **add_task** - Create a new todo task
   - Use when: User wants to add, create, or remember something
   - Always confirm: "I've added '[task title]' to your task list!"

2. **list_tasks** - Retrieve and display tasks
   - Use when: User wants to see, view, list, or check their tasks
   - Filter by status if requested (all/pending/completed)
   - Present tasks in a clear, organized format

3. **complete_task** - Mark a task as done
   - Use when: User wants to complete, finish, or mark a task as done
   - Always confirm: "Great job! I've marked '[task title]' as completed!"

4. **update_task** - Modify task details
   - Use when: User wants to change, edit, or update a task
   - Always confirm: "I've updated the task to '[new details]'"

5. **delete_task** - Remove a task
   - Use when: User wants to delete, remove, or get rid of a task
   - Always confirm: "I've deleted '[task title]' from your list"

## RESPONSE GUIDELINES

### When Using Tools:
1. **Always provide confirmation** after executing a tool
2. **Be specific** - mention the task title or details
3. **Be encouraging** - celebrate completions and progress
4. **Handle errors gracefully** - if a tool fails, explain why and suggest alternatives

### When Chatting (No Tools):
1. Answer questions about task management
2. Provide productivity tips
3. Help users understand what you can do
4. Be conversational and friendly

### Examples of Good Responses:

**Adding a task:**
User: "Add a task to buy groceries"
You: "I've added 'buy groceries' to your task list! 🛒"

**Listing tasks:**
User: "Show me my tasks"
You: "Here are your current tasks:
1. Buy groceries (pending)
2. Finish report (pending)
3. Call mom (completed)

You have 2 pending tasks. Keep it up!"

**Completing a task:**
User: "Mark task 1 as done"
You: "Awesome! I've marked 'Buy groceries' as completed! 🎉"

**General chat:**
User: "What can you do?"
You: "I'm your personal task assistant! I can help you:
- Add new tasks
- View your task list
- Mark tasks as completed
- Update task details
- Delete tasks you no longer need

Just tell me what you'd like to do!"

## IMPORTANT RULES
1. **Only perform actions the user explicitly requests**
2. **Always confirm actions with specific details**
3. **Be encouraging and positive**
4. **If unsure, ask for clarification**
5. **Handle errors gracefully and suggest solutions**
6. **Keep responses concise but friendly**

Remember: Your goal is to make task management effortless and enjoyable for the user!"""
        }

    def _call_ai_with_fallback(self, messages: List[Dict[str, str]]) -> Tuple[str, List[Dict], bool]:
        """
        Try calling AI providers in order until one succeeds.

        Returns:
            Tuple of (response_text, tool_calls, all_providers_exhausted)
        """
        for provider_name, provider in self.providers:
            try:
                logger.info(f"Trying {provider_name}...")
                content, tool_calls, quota_exceeded = provider.call_ai(messages, self.available_tools)

                if quota_exceeded:
                    logger.warning(f"{provider_name} quota exceeded, trying next provider...")
                    continue

                logger.info(f"{provider_name} succeeded")
                return content, tool_calls, False

            except Exception as e:
                logger.error(f"{provider_name} failed: {e}")
                continue

        # All providers failed or exhausted
        logger.error("All AI providers exhausted or failed")
        return "", [], True

    def run_chat_request(
        self,
        user_id: int,
        message_content: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Run a conversation with the AI agent, including tool calls.

        Args:
            user_id: ID of the authenticated user
            message_content: The user's message to the AI
            conversation_id: Optional ID of existing conversation (creates new if None)

        Returns:
            Dict containing the assistant response and any tool invocations that occurred
        """
        try:
            # Create a database session
            db_session = Session(engine)

            try:
                # Validate user exists
                user = db_session.get(User, user_id)
                if not user:
                    return {
                        "success": False,
                        "data": None,
                        "error": {
                            "code": "USER_NOT_FOUND",
                            "message": f"User with ID {user_id} does not exist",
                            "details": {"user_id": user_id}
                        }
                    }

                # Get or create conversation
                conversation = None
                if conversation_id:
                    conversation = db_session.get(Conversation, conversation_id)
                    if not conversation or conversation.user_id != user_id:
                        return {
                            "success": False,
                            "data": None,
                            "error": {
                                "code": "CONVERSATION_NOT_FOUND",
                                "message": f"Conversation with ID {conversation_id} does not exist or does not belong to user",
                                "details": {"conversation_id": conversation_id, "user_id": user_id}
                            }
                        }
                else:
                    # Create new conversation
                    title = message_content[:50] + "..." if len(message_content) > 50 else message_content
                    conversation = Conversation(user_id=user_id, title=title)
                    db_session.add(conversation)
                    db_session.commit()
                    db_session.refresh(conversation)

                # Save user message to database
                user_message = Message(
                    conversation_id=conversation.id,
                    role="user",
                    content=message_content
                )
                db_session.add(user_message)
                db_session.commit()
                db_session.refresh(user_message)

                # ============================================================
                # HYBRID ROUTING: Try local task parser first, then AI fallback
                # ============================================================

                # Step 1: Try to parse as a task command (LOCAL - NO API CALL)
                intent, params = self.task_parser.parse(message_content)

                if intent:
                    # Task command detected! Execute locally without AI
                    logger.info(f"🚀 LOCAL EXECUTION: {intent} with params {params}")

                    # Add user_id to params
                    params["user_id"] = user_id

                    # Special handling: If task_name is provided instead of task_id, look it up
                    if "task_name" in params and intent in ["complete_task", "update_task", "delete_task"]:
                        task_name = params.pop("task_name")
                        logger.info(f"Looking up task by name: '{task_name}'")

                        # Get all user's tasks to find matching name
                        try:
                            list_result = self.tools.list_tasks(user_id=user_id, status="all")
                            if list_result["success"] and list_result["data"]:
                                tasks = list_result["data"]
                                # Find task by name (case-insensitive partial match)
                                matching_task = None
                                for task in tasks:
                                    if task_name.lower() in task.get("title", "").lower():
                                        matching_task = task
                                        break

                                if matching_task:
                                    params["task_id"] = matching_task["id"]
                                    logger.info(f"Found task: id={matching_task['id']}, title='{matching_task['title']}'")
                                else:
                                    # Task not found
                                    assistant_content = f"❌ I couldn't find a task named '{task_name}'. Try 'Show me my tasks' to see all your tasks."
                                    assistant_message = Message(
                                        conversation_id=conversation.id,
                                        role="assistant",
                                        content=assistant_content
                                    )
                                    db_session.add(assistant_message)
                                    db_session.commit()

                                    return {
                                        "success": True,
                                        "data": {
                                            "conversation_id": conversation.id,
                                            "response": assistant_content,
                                            "tool_calls": []
                                        },
                                        "error": None
                                    }
                        except Exception as e:
                            logger.error(f"Error looking up task by name: {e}")
                            # Fall back to AI agent
                            intent = None

                    # Execute the tool
                    tool_result = None
                    tool_method_name = intent  # Intent names match tool method names

                    if hasattr(self.tools, tool_method_name):
                        tool_method = getattr(self.tools, tool_method_name)
                        tool_result = tool_method(**params)
                    else:
                        tool_result = {
                            "success": False,
                            "data": None,
                            "error": {
                                "code": "UNKNOWN_TOOL",
                                "message": f"Unknown tool: {tool_method_name}",
                                "details": {"tool_name": tool_method_name}
                            }
                        }

                    # Generate friendly confirmation message
                    assistant_content = self.task_parser.generate_confirmation(
                        intent, params, tool_result
                    )

                    # Save assistant response
                    assistant_message = Message(
                        conversation_id=conversation.id,
                        role="assistant",
                        content=assistant_content
                    )
                    db_session.add(assistant_message)
                    db_session.commit()
                    db_session.refresh(assistant_message)

                    # Return result
                    logger.info(f"✅ LOCAL EXECUTION SUCCESS: {assistant_content[:50]}...")
                    return {
                        "success": True,
                        "data": {
                            "conversation_id": conversation.id,
                            "response": assistant_content,
                            "tool_calls": [{
                                "name": intent,
                                "arguments": params,
                                "result": tool_result
                            }]
                        },
                        "error": None
                    }

                # Step 2: No task intent detected, use AI agent for conversation
                logger.info("🤖 AI AGENT: No task intent detected, using AI for conversation")

                # Load conversation history for context
                history_messages = db_session.exec(
                    select(Message)
                    .where(Message.conversation_id == conversation.id)
                    .order_by(Message.timestamp)
                ).all()

                # Format messages for the AI agent
                formatted_messages = [self.system_prompt]

                for msg in history_messages:
                    formatted_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

                # Call the AI with fallback
                assistant_content, tool_calls, all_exhausted = self._call_ai_with_fallback(formatted_messages)

                # If all providers are exhausted, return friendly message
                if all_exhausted:
                    friendly_message = "Hey dude! 😅 I'm currently out of battery. Please try a little later when I've recharged!"

                    assistant_message = Message(
                        conversation_id=conversation.id,
                        role="assistant",
                        content=friendly_message
                    )
                    db_session.add(assistant_message)
                    db_session.commit()

                    return {
                        "success": True,
                        "data": {
                            "conversation_id": conversation.id,
                            "response": friendly_message,
                            "tool_calls": []
                        },
                        "error": None
                    }

                # Execute any tool calls
                tool_results = []
                if tool_calls:
                    for tool_call in tool_calls:
                        function_name = tool_call["name"]
                        function_args = tool_call["arguments"]

                        # Add user_id to function arguments since all tools require it
                        function_args["user_id"] = user_id

                        # Execute the appropriate tool
                        tool_result = None
                        if hasattr(self.tools, function_name):
                            tool_method = getattr(self.tools, function_name)
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

                        tool_results.append({
                            "name": function_name,
                            "arguments": function_args,
                            "result": tool_result
                        })

                    # If tools were called but no text response, generate a confirmation locally
                    if not assistant_content or assistant_content.strip() == "":
                        logger.info("No text response from AI after tool calls, generating local confirmation")

                        # Generate friendly confirmation messages based on tool results
                        confirmations = []
                        for tr in tool_results:
                            function_name = tr["name"]
                            result = tr["result"]

                            if result["success"]:
                                data = result.get("data", {})

                                if function_name == "add_task":
                                    title = tr["arguments"].get("title", "task")
                                    confirmations.append(f"✅ I've added '{title}' to your task list!")

                                elif function_name == "list_tasks":
                                    tasks = data if isinstance(data, list) else []
                                    if not tasks:
                                        confirmations.append("You don't have any tasks yet. Would you like to add one?")
                                    else:
                                        pending = [t for t in tasks if not t.get("completed", False)]
                                        completed = [t for t in tasks if t.get("completed", False)]

                                        task_list = "Here are your tasks:\n\n"
                                        for i, task in enumerate(tasks, 1):
                                            status = "✅" if task.get("completed") else "📝"
                                            task_list += f"{i}. {status} {task.get('title', 'Untitled')}\n"

                                        task_list += f"\n📊 {len(pending)} pending, {len(completed)} completed"
                                        confirmations.append(task_list)

                                elif function_name == "complete_task":
                                    task_id = tr["arguments"].get("task_id")
                                    task_title = data.get("title", f"task {task_id}")
                                    confirmations.append(f"🎉 Awesome! I've marked '{task_title}' as completed!")

                                elif function_name == "update_task":
                                    new_title = tr["arguments"].get("title", "")
                                    new_desc = tr["arguments"].get("description", "")
                                    updated_text = new_title or new_desc or "the task"
                                    confirmations.append(f"✏️ I've updated the task to '{updated_text}'")

                                elif function_name == "delete_task":
                                    task_id = tr["arguments"].get("task_id")
                                    confirmations.append(f"🗑️ I've deleted task {task_id} from your list")

                            else:
                                # Handle errors
                                error_msg = result.get("error", {}).get("message", "Unknown error")
                                confirmations.append(f"❌ Sorry, I couldn't complete that action: {error_msg}")

                        assistant_content = "\n\n".join(confirmations) if confirmations else "Task completed successfully!"

                # Create assistant response message
                assistant_message = Message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=assistant_content
                )
                db_session.add(assistant_message)
                db_session.commit()
                db_session.refresh(assistant_message)

                # Prepare the response
                result = {
                    "success": True,
                    "data": {
                        "conversation_id": conversation.id,
                        "response": assistant_content,
                        "tool_calls": tool_results
                    },
                    "error": None
                }

                return result

            finally:
                # Close the database session
                db_session.close()

        except Exception as e:
            logger.error(f"Error in run_chat_request: {e}", exc_info=True)
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": f"Failed to process chat request: {str(e)}",
                    "details": {"exception": str(e)}
                }
            }

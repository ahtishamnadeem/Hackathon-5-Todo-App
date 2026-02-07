"""Local task command parser for instant task operations without AI API calls."""

import re
from typing import Optional, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class TaskCommandParser:
    """
    Parses user messages to detect task-related intents and extract parameters.
    Uses pattern matching to avoid AI API calls for common task operations.
    """

    def __init__(self):
        """Initialize the parser with intent patterns."""

        # Patterns for adding tasks
        self.add_patterns = [
            r"(?:add|create|new|make)\s+(?:a\s+)?task\s+(?:to\s+)?(.+)",
            r"(?:remind me to|i need to|todo)\s+(.+)",
            r"(?:add|create)\s+(.+)\s+to\s+(?:my\s+)?(?:task\s+)?list",
        ]

        # Patterns for listing tasks
        self.list_patterns = [
            r"(?:show|list|display|get|view)\s+(?:me\s+)?(?:my\s+)?(?:all\s+)?tasks?",
            r"what\s+(?:are\s+)?(?:my\s+)?tasks?",
            r"(?:do\s+)?i\s+have\s+(?:any\s+)?tasks?",
            r"tasks?\s+list",
            r"show\s+(?:me\s+)?(?:my\s+)?(?:pending|completed)\s+tasks?",
        ]

        # Patterns for completing tasks
        self.complete_patterns = [
            # With task ID
            (r"(?:mark|set|make)\s+task\s+(\d+)\s+(?:as\s+)?(?:done|complete|completed|finished)", "id"),
            (r"(?:complete|finish|done\s+with)\s+task\s+(\d+)", "id"),
            (r"task\s+(\d+)\s+(?:is\s+)?(?:done|complete|completed|finished)", "id"),
            # With task name/title
            (r"(?:mark|set|make)\s+task\s+(?:as\s+)?(?:done|complete|completed|finished)\s+['\"](.+?)['\"]", "name"),
            (r"(?:mark|set|make)\s+['\"](.+?)['\"](?:\s+as\s+)?(?:done|complete|completed|finished)", "name"),
            (r"(?:complete|finish)\s+(?:task\s+)?['\"](.+?)['\"]", "name"),
            (r"(?:mark|complete|finish)\s+(?:task\s+)?(?:as\s+)?(?:done|complete|completed|finished)\s+(.+)", "name"),
        ]

        # Patterns for updating tasks
        self.update_patterns = [
            r"(?:update|change|edit|modify)\s+task\s+(\d+)\s+to\s+(.+)",
            r"(?:rename|change)\s+task\s+(\d+)\s+(.+)",
        ]

        # Patterns for deleting tasks
        self.delete_patterns = [
            r"(?:delete|remove|erase)\s+task\s+(\d+)",
            r"(?:get\s+rid\s+of|cancel)\s+task\s+(\d+)",
        ]

    def parse(self, message: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Parse a user message to detect intent and extract parameters.

        Args:
            message: The user's message

        Returns:
            Tuple of (intent, parameters) or (None, None) if no intent detected

        Intents:
            - "add_task": {"title": str, "description": str (optional)}
            - "list_tasks": {"status": "all"|"pending"|"completed"}
            - "complete_task": {"task_id": int}
            - "update_task": {"task_id": int, "title": str}
            - "delete_task": {"task_id": int}
        """
        message_lower = message.lower().strip()

        # Try to match add task patterns
        for pattern in self.add_patterns:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                logger.info(f"Detected add_task intent: title='{title}'")
                return "add_task", {"title": title}

        # Try to match complete task patterns
        for pattern, param_type in self.complete_patterns:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                if param_type == "id":
                    task_id = int(match.group(1))
                    logger.info(f"Detected complete_task intent: task_id={task_id}")
                    return "complete_task", {"task_id": task_id}
                else:  # param_type == "name"
                    task_name = match.group(1).strip().strip('"\'')
                    logger.info(f"Detected complete_task intent: task_name='{task_name}'")
                    return "complete_task", {"task_name": task_name}

        # Try to match update task patterns
        for pattern in self.update_patterns:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                task_id = int(match.group(1))
                new_title = match.group(2).strip()
                logger.info(f"Detected update_task intent: task_id={task_id}, title='{new_title}'")
                return "update_task", {"task_id": task_id, "title": new_title}

        # Try to match delete task patterns
        for pattern in self.delete_patterns:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                task_id = int(match.group(1))
                logger.info(f"Detected delete_task intent: task_id={task_id}")
                return "delete_task", {"task_id": task_id}

        # Try to match list task patterns
        for pattern in self.list_patterns:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                # Check if user wants pending or completed
                status = "all"
                if "pending" in message_lower:
                    status = "pending"
                elif "completed" in message_lower or "done" in message_lower:
                    status = "completed"

                logger.info(f"Detected list_tasks intent: status='{status}'")
                return "list_tasks", {"status": status}

        # No intent detected, fallback to AI
        logger.info("No task intent detected, will use AI agent")
        return None, None

    def generate_confirmation(
        self,
        intent: str,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> str:
        """
        Generate a friendly confirmation message for a task operation.

        Args:
            intent: The detected intent
            params: The extracted parameters
            result: The result from the tool execution

        Returns:
            A friendly confirmation message
        """
        if not result.get("success"):
            error_msg = result.get("error", {}).get("message", "Unknown error")
            return f"❌ Sorry, I couldn't complete that action: {error_msg}"

        data = result.get("data", {})

        if intent == "add_task":
            title = params.get("title", "task")
            return f"✅ I've added '{title}' to your task list!"

        elif intent == "list_tasks":
            tasks = data if isinstance(data, list) else []
            if not tasks:
                return "You don't have any tasks yet. Would you like to add one?"

            pending = [t for t in tasks if not t.get("completed", False)]
            completed = [t for t in tasks if t.get("completed", False)]

            task_list = "Here are your tasks:\n\n"
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get("completed") else "📝"
                task_list += f"{i}. {status} {task.get('title', 'Untitled')}\n"

            task_list += f"\n📊 {len(pending)} pending, {len(completed)} completed"
            return task_list

        elif intent == "complete_task":
            task_id = params.get("task_id")
            task_title = data.get("title", f"task {task_id}")
            return f"🎉 Awesome! I've marked '{task_title}' as completed!"

        elif intent == "update_task":
            new_title = params.get("title", "")
            return f"✏️ I've updated the task to '{new_title}'"

        elif intent == "delete_task":
            task_id = params.get("task_id")
            return f"🗑️ I've deleted task {task_id} from your list"

        return "Task completed successfully!"

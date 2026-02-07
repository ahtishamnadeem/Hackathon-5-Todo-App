"""MCP task management tools implementation."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from ...models.todo import Todo
from ...models.user import User
from .validators import (
    validate_add_task_params, validate_list_tasks_params, validate_complete_task_params,
    validate_update_task_params, validate_delete_task_params,
    AddTaskParams, ListTasksParams, CompleteTaskParams, UpdateTaskParams, DeleteTaskParams
)
from ...database import engine

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


class AddTaskTool(BaseMCPTaskTool):
    """MCP tool to add a new task."""

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the add_task operation."""
        logger.info(f"Executing add_task for user_id: {params.get('user_id')}")

        try:
            validated_params = validate_add_task_params(params)

            # Verify user exists
            if not self.validate_user_exists(validated_params.user_id):
                logger.warning(f"Unauthorized access attempt: User {validated_params.user_id} does not exist")
                return self.format_error_response(
                    "UNAUTHORIZED",
                    f"User with ID {validated_params.user_id} does not exist",
                    {"user_id": validated_params.user_id}
                )

            # Create new task
            todo = Todo(
                title=validated_params.title,
                description=validated_params.description,
                completed=False,  # Default to false as specified
                user_id=validated_params.user_id
            )

            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)

            logger.info(f"Successfully created task {todo.id} for user {validated_params.user_id}")

            return self.format_success_response({
                "id": todo.id,
                "status": "created",
                "title": todo.title
            })

        except ValueError as e:
            self.db.rollback()
            logger.error(f"Validation error in add_task: {str(e)}")
            return self.format_error_response(
                "VALIDATION_ERROR",
                str(e),
                {"invalid_params": params}
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database error in add_task: {str(e)}")
            return self.format_error_response(
                "DATABASE_ERROR",
                f"Failed to create task: {str(e)}",
                {"exception": str(e)}
            )


class ListTasksTool(BaseMCPTaskTool):
    """MCP tool to list tasks for a user."""

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the list_tasks operation."""
        logger.info(f"Executing list_tasks for user_id: {params.get('user_id')}, status: {params.get('status')}")

        try:
            validated_params = validate_list_tasks_params(params)

            # Verify user exists
            if not self.validate_user_exists(validated_params.user_id):
                logger.warning(f"Unauthorized access attempt: User {validated_params.user_id} does not exist")
                return self.format_error_response(
                    "UNAUTHORIZED",
                    f"User with ID {validated_params.user_id} does not exist",
                    {"user_id": validated_params.user_id}
                )

            # Build query with user_id filter
            query = select(Todo).where(Todo.user_id == validated_params.user_id)

            # Apply status filter if provided
            if validated_params.status and validated_params.status != 'all':
                if validated_params.status == 'pending':
                    query = query.where(Todo.completed == False)
                elif validated_params.status == 'completed':
                    query = query.where(Todo.completed == True)

            # Sort by creation time (ascending) as specified
            query = query.order_by(Todo.created_at.asc())

            todos = self.db.exec(query).all()

            # Format response
            tasks_data = [
                {
                    "id": todo.id,
                    "title": todo.title,
                    "completed": todo.completed
                }
                for todo in todos
            ]

            logger.info(f"Successfully retrieved {len(tasks_data)} tasks for user {validated_params.user_id}")

            return self.format_success_response(tasks_data)

        except ValueError as e:
            logger.error(f"Validation error in list_tasks: {str(e)}")
            return self.format_error_response(
                "VALIDATION_ERROR",
                str(e),
                {"invalid_params": params}
            )
        except Exception as e:
            logger.error(f"Database error in list_tasks: {str(e)}")
            return self.format_error_response(
                "DATABASE_ERROR",
                f"Failed to list tasks: {str(e)}",
                {"exception": str(e)}
            )


class CompleteTaskTool(BaseMCPTaskTool):
    """MCP tool to complete a task."""

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete_task operation."""
        logger.info(f"Executing complete_task for user_id: {params.get('user_id')}, task_id: {params.get('task_id')}")

        try:
            validated_params = validate_complete_task_params(params)

            # Verify user exists
            if not self.validate_user_exists(validated_params.user_id):
                logger.warning(f"Unauthorized access attempt: User {validated_params.user_id} does not exist")
                return self.format_error_response(
                    "UNAUTHORIZED",
                    f"User with ID {validated_params.user_id} does not exist",
                    {"user_id": validated_params.user_id}
                )

            # Verify task exists and belongs to user
            if not self.validate_task_ownership(validated_params.task_id, validated_params.user_id):
                logger.warning(f"Task access denied: Task {validated_params.task_id} does not belong to user {validated_params.user_id}")
                return self.format_error_response(
                    "NOT_FOUND",
                    f"Task with ID {validated_params.task_id} does not exist or does not belong to user",
                    {"task_id": validated_params.task_id, "user_id": validated_params.user_id}
                )

            # Get the task and update completion status
            todo = self.db.get(Todo, validated_params.task_id)
            todo.completed = True
            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)

            logger.info(f"Successfully completed task {todo.id} for user {validated_params.user_id}")

            return self.format_success_response({
                "task_id": todo.id,
                "status": "completed",
                "title": todo.title
            })

        except ValueError as e:
            self.db.rollback()
            logger.error(f"Validation error in complete_task: {str(e)}")
            return self.format_error_response(
                "VALIDATION_ERROR",
                str(e),
                {"invalid_params": params}
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database error in complete_task: {str(e)}")
            return self.format_error_response(
                "DATABASE_ERROR",
                f"Failed to complete task: {str(e)}",
                {"exception": str(e)}
            )


class UpdateTaskTool(BaseMCPTaskTool):
    """MCP tool to update a task."""

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the update_task operation."""
        logger.info(f"Executing update_task for user_id: {params.get('user_id')}, task_id: {params.get('task_id')}")

        try:
            validated_params = validate_update_task_params(params)

            # Verify user exists
            if not self.validate_user_exists(validated_params.user_id):
                logger.warning(f"Unauthorized access attempt: User {validated_params.user_id} does not exist")
                return self.format_error_response(
                    "UNAUTHORIZED",
                    f"User with ID {validated_params.user_id} does not exist",
                    {"user_id": validated_params.user_id}
                )

            # Verify task exists and belongs to user
            if not self.validate_task_ownership(validated_params.task_id, validated_params.user_id):
                logger.warning(f"Task access denied: Task {validated_params.task_id} does not belong to user {validated_params.user_id}")
                return self.format_error_response(
                    "NOT_FOUND",
                    f"Task with ID {validated_params.task_id} does not exist or does not belong to user",
                    {"task_id": validated_params.task_id, "user_id": validated_params.user_id}
                )

            # Get the task and update only provided fields
            todo = self.db.get(Todo, validated_params.task_id)

            if validated_params.title is not None:
                todo.title = validated_params.title
            if validated_params.description is not None:
                todo.description = validated_params.description

            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)

            logger.info(f"Successfully updated task {todo.id} for user {validated_params.user_id}")

            return self.format_success_response({
                "task_id": todo.id,
                "status": "updated",
                "title": todo.title
            })

        except ValueError as e:
            self.db.rollback()
            logger.error(f"Validation error in update_task: {str(e)}")
            return self.format_error_response(
                "VALIDATION_ERROR",
                str(e),
                {"invalid_params": params}
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database error in update_task: {str(e)}")
            return self.format_error_response(
                "DATABASE_ERROR",
                f"Failed to update task: {str(e)}",
                {"exception": str(e)}
            )


class DeleteTaskTool(BaseMCPTaskTool):
    """MCP tool to delete a task."""

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the delete_task operation."""
        logger.info(f"Executing delete_task for user_id: {params.get('user_id')}, task_id: {params.get('task_id')}")

        try:
            validated_params = validate_delete_task_params(params)

            # Verify user exists
            if not self.validate_user_exists(validated_params.user_id):
                logger.warning(f"Unauthorized access attempt: User {validated_params.user_id} does not exist")
                return self.format_error_response(
                    "UNAUTHORIZED",
                    f"User with ID {validated_params.user_id} does not exist",
                    {"user_id": validated_params.user_id}
                )

            # Verify task exists and belongs to user
            if not self.validate_task_ownership(validated_params.task_id, validated_params.user_id):
                logger.warning(f"Task access denied: Task {validated_params.task_id} does not belong to user {validated_params.user_id}")
                return self.format_error_response(
                    "NOT_FOUND",
                    f"Task with ID {validated_params.task_id} does not exist or does not belong to user",
                    {"task_id": validated_params.task_id, "user_id": validated_params.user_id}
                )

            # Get the task and delete it
            todo = self.db.get(Todo, validated_params.task_id)
            self.db.delete(todo)
            self.db.commit()

            logger.info(f"Successfully deleted task {todo.id} for user {validated_params.user_id}")

            return self.format_success_response({
                "task_id": todo.id,
                "status": "deleted",
                "title": todo.title
            })

        except ValueError as e:
            self.db.rollback()
            logger.error(f"Validation error in delete_task: {str(e)}")
            return self.format_error_response(
                "VALIDATION_ERROR",
                str(e),
                {"invalid_params": params}
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database error in delete_task: {str(e)}")
            return self.format_error_response(
                "DATABASE_ERROR",
                f"Failed to delete task: {str(e)}",
                {"exception": str(e)}
            )
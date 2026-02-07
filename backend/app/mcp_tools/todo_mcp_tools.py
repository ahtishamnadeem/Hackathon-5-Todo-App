"""MCP tools for todo management operations."""

from typing import Dict, Any, Optional
from sqlmodel import Session, select
from ..models.todo import Todo
from ..models.user import User
from ..database import engine


class TodoMCPTasks:
    """
    MCP tools for todo operations that follow stateless design pattern and require user_id for every operation.
    These tools maintain clear separation between AI reasoning and execution.
    """

    def __init__(self):
        """Initialize the todo MCP tools."""
        pass

    def add_task(self, title: str, description: Optional[str] = None, user_id: int = None) -> Dict[str, Any]:
        """
        Create a new todo task for the specified user.

        Args:
            title: Title of the task
            description: Optional description of the task
            user_id: ID of the user creating the task

        Returns:
            Dict with success status and task information
        """
        if not user_id:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "user_id is required for this operation",
                    "details": {"field": "user_id"}
                }
            }

        # Create a database session
        db_session = Session(engine)
        try:
            # Verify user exists
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

            # Create new task
            todo = Todo(
                title=title,
                description=description,
                completed=False,  # Default to false as specified
                user_id=user_id
            )

            db_session.add(todo)
            db_session.commit()
            db_session.refresh(todo)

            return {
                "success": True,
                "data": {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "user_id": todo.user_id
                },
                "error": None
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Failed to create task: {str(e)}",
                    "details": {"exception": str(e)}
                }
            }
        finally:
            db_session.close()

    def list_tasks(self, status: Optional[str] = None, user_id: int = None) -> Dict[str, Any]:
        """
        Retrieve the user's todo tasks with optional filtering.

        Args:
            status: Optional filter for completion status ("all", "pending", "completed")
            user_id: ID of the user whose tasks to retrieve

        Returns:
            Dict with success status and list of user's tasks
        """
        if not user_id:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "user_id is required for this operation",
                    "details": {"field": "user_id"}
                }
            }

        # Create a database session
        db_session = Session(engine)
        try:
            # Verify user exists
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

            # Build query with user_id filter
            query = select(Todo).where(Todo.user_id == user_id)

            # Apply status filter if provided
            if status and status != "all":
                if status == "pending":
                    query = query.where(Todo.completed == False)
                elif status == "completed":
                    query = query.where(Todo.completed == True)

            # Sort by creation time (ascending) as specified
            query = query.order_by(Todo.created_at.asc())

            todos = db_session.exec(query).all()

            return {
                "success": True,
                "data": [
                    {
                        "id": todo.id,
                        "title": todo.title,
                        "description": todo.description,
                        "completed": todo.completed
                    }
                    for todo in todos
                ],
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Failed to list tasks: {str(e)}",
                    "details": {"exception": str(e)}
                }
            }
        finally:
            db_session.close()

    def complete_task(self, task_id: int, completed: bool = True, user_id: int = None) -> Dict[str, Any]:
        """
        Mark a specific task as completed or uncompleted.

        Args:
            task_id: ID of the task to update
            completed: Whether the task is completed (default True)
            user_id: ID of the user requesting the update

        Returns:
            Dict with success status and updated task information
        """
        if not user_id:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "user_id is required for this operation",
                    "details": {"field": "user_id"}
                }
            }

        # Create a database session
        db_session = Session(engine)
        try:
            # Verify user exists
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

            # Verify task exists and belongs to user
            todo = db_session.get(Todo, task_id)
            if not todo:
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with ID {task_id} does not exist",
                        "details": {"task_id": task_id}
                    }
                }

            if todo.user_id != user_id:
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "NOT_FOUND",  # Use 404 instead of 403 to prevent data enumeration
                        "message": f"Task with ID {task_id} does not belong to user",
                        "details": {"task_id": task_id, "user_id": user_id}
                    }
                }

            # Update completion status
            todo.completed = completed
            db_session.add(todo)
            db_session.commit()
            db_session.refresh(todo)

            return {
                "success": True,
                "data": {
                    "id": todo.id,
                    "title": todo.title,
                    "completed": todo.completed
                },
                "error": None
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Failed to complete task: {str(e)}",
                    "details": {"exception": str(e)}
                }
            }
        finally:
            db_session.close()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, user_id: int = None) -> Dict[str, Any]:
        """
        Modify an existing task's title or description.

        Args:
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            user_id: ID of the user requesting the update

        Returns:
            Dict with success status and updated task information
        """
        if not user_id:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "user_id is required for this operation",
                    "details": {"field": "user_id"}
                }
            }

        # Create a database session
        db_session = Session(engine)
        try:
            # Verify user exists
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

            # Verify task exists and belongs to user
            todo = db_session.get(Todo, task_id)
            if not todo:
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with ID {task_id} does not exist",
                        "details": {"task_id": task_id}
                    }
                }

            if todo.user_id != user_id:
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "NOT_FOUND",  # Use 404 instead of 403 to prevent data enumeration
                        "message": f"Task with ID {task_id} does not belong to user",
                        "details": {"task_id": task_id, "user_id": user_id}
                    }
                }

            # Update only provided fields
            if title is not None:
                todo.title = title
            if description is not None:
                todo.description = description

            db_session.add(todo)
            db_session.commit()
            db_session.refresh(todo)

            return {
                "success": True,
                "data": {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed
                },
                "error": None
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Failed to update task: {str(e)}",
                    "details": {"exception": str(e)}
                }
            }
        finally:
            db_session.close()

    def delete_task(self, task_id: int, user_id: int = None) -> Dict[str, Any]:
        """
        Remove a specific task.

        Args:
            task_id: ID of the task to delete
            user_id: ID of the user requesting the deletion

        Returns:
            Dict with success status
        """
        if not user_id:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "user_id is required for this operation",
                    "details": {"field": "user_id"}
                }
            }

        # Create a database session
        db_session = Session(engine)
        try:
            # Verify user exists
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

            # Verify task exists and belongs to user
            todo = db_session.get(Todo, task_id)
            if not todo:
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with ID {task_id} does not exist",
                        "details": {"task_id": task_id}
                    }
                }

            if todo.user_id != user_id:
                return {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "NOT_FOUND",  # Use 404 instead of 403 to prevent data enumeration
                        "message": f"Task with ID {task_id} does not belong to user",
                        "details": {"task_id": task_id, "user_id": user_id}
                    }
                }

            # Delete the task
            db_session.delete(todo)
            db_session.commit()

            return {
                "success": True,
                "data": {
                    "id": todo.id,
                    "status": "deleted",
                    "title": todo.title
                },
                "error": None
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Failed to delete task: {str(e)}",
                    "details": {"exception": str(e)}
                }
            }
        finally:
            db_session.close()
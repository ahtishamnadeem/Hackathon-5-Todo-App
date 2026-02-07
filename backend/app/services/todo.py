"""Todo service layer with user isolation."""

from sqlmodel import Session, select
from typing import List, Optional

from app.models.todo import Todo
from app.models.user import User
from app.utils.errors import NotFoundException, UnauthorizedException


def create_todo(
    title: str,
    description: Optional[str],
    user_id: int,
    session: Session,
    priority: str = "medium",
    tags: Optional[str] = None
) -> Todo:
    """Create a new todo for the authenticated user.

    Args:
        title: Todo title (required, non-empty)
        description: Todo description (optional)
        user_id: ID of the authenticated user creating the todo
        session: Database session
        priority: Task priority (low, medium, high) - default: medium
        tags: Comma-separated tags (optional)

    Returns:
        Created Todo instance

    Raises:
        ValidationException: If title is empty or too long

    Security (FR-015, FR-016):
        - Assigns todo to the authenticated user (user_id from JWT)
        - Does not allow client to specify user_id in request body
    """
    # Validate title (non-empty as per FR-015)
    if not title or not title.strip():
        from app.utils.errors import ValidationException
        raise ValidationException("Todo title cannot be empty")

    # Validate priority
    if priority not in ["low", "medium", "high"]:
        priority = "medium"

    # Create todo assigned to the authenticated user
    todo = Todo(
        title=title.strip(),
        description=description.strip() if description else None,
        user_id=user_id,  # Assigned from JWT, not from request body (FR-016)
        completed=False,
        priority=priority,
        tags=tags.strip() if tags else None
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


def get_user_todos(user_id: int, session: Session) -> List[Todo]:
    """Get all todos for the authenticated user, ordered by creation date descending.

    Args:
        user_id: ID of the authenticated user
        session: Database session

    Returns:
        List of todos owned by the user, ordered by created_at DESC (FR-017)

    Security (FR-018, FR-019):
        - Filters todos by user_id to enforce data isolation
        - Only returns todos owned by the authenticated user
        - Never returns other users' todos
    """
    # Query todos filtered by user_id for security (FR-018, FR-019)
    statement = (
        select(Todo)
        .where(Todo.user_id == user_id)
        .order_by(Todo.created_at.desc())  # Order by created_at DESC (FR-017)
    )

    todos = session.exec(statement).all()
    return todos


def get_todo_by_id(todo_id: int, user_id: int, session: Session) -> Optional[Todo]:
    """Get a specific todo by ID for the authenticated user.

    Args:
        todo_id: ID of the todo to retrieve
        user_id: ID of the authenticated user
        session: Database session

    Returns:
        Todo instance if it exists and is owned by the user, None otherwise

    Security (FR-020):
        - Queries by both todo_id AND user_id for ownership verification
        - Returns None if todo doesn't exist OR doesn't belong to user
        - Prevents users from accessing other users' todos
    """
    # Query by both ID and user_id for security (FR-020)
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(statement).first()

    return todo


def update_todo(
    todo_id: int,
    user_id: int,
    session: Session,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tags: Optional[str] = None
) -> Optional[Todo]:
    """Update a todo if it belongs to the authenticated user.

    Args:
        todo_id: ID of the todo to update
        user_id: ID of the authenticated user
        session: Database session
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
        priority: New priority (low, medium, high) (optional)
        tags: New tags (comma-separated) (optional)

    Returns:
        Updated Todo instance if successful, None if not found or not owned

    Security (FR-021):
        - Verifies ownership by checking user_id matches
        - Only updates fields that are provided (partial update)
    """
    # Get the todo ensuring it belongs to the user
    todo = get_todo_by_id(todo_id, user_id, session)

    if not todo:
        return None

    # Update only the fields that are provided
    if title is not None:
        if not title.strip():
            from app.utils.errors import ValidationException
            raise ValidationException("Todo title cannot be empty")
        todo.title = title.strip()

    if description is not None:
        todo.description = description.strip() if description else None

    if completed is not None:
        todo.completed = completed

    if priority is not None:
        if priority in ["low", "medium", "high"]:
            todo.priority = priority

    if tags is not None:
        todo.tags = tags.strip() if tags else None

    # Update the timestamp
    from datetime import datetime
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


def toggle_todo_complete(todo_id: int, user_id: int, session: Session) -> Optional[Todo]:
    """Toggle the completion status of a todo.

    Args:
        todo_id: ID of the todo to toggle
        user_id: ID of the authenticated user
        session: Database session

    Returns:
        Updated Todo instance if successful, None if not found or not owned

    Security (FR-022):
        - Verifies ownership before toggling
        - Only allows user to toggle their own todos
    """
    # Get the todo ensuring it belongs to the user
    todo = get_todo_by_id(todo_id, user_id, session)

    if not todo:
        return None

    # Toggle completion status
    todo.completed = not todo.completed

    # Update the timestamp
    from datetime import datetime
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


def delete_todo(todo_id: int, user_id: int, session: Session) -> bool:
    """Delete a todo if it belongs to the authenticated user.

    Args:
        todo_id: ID of the todo to delete
        user_id: ID of the authenticated user
        session: Database session

    Returns:
        True if deletion was successful, False if todo not found or not owned

    Security (FR-023):
        - Verifies ownership before deletion
        - Only allows user to delete their own todos
        - Uses both ID and user_id for security check
    """
    # Get the todo ensuring it belongs to the user
    todo = get_todo_by_id(todo_id, user_id, session)

    if not todo:
        return False

    # Delete the todo
    session.delete(todo)
    session.commit()

    return True

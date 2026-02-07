"""Todo API endpoints with user isolation."""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.middleware.auth import get_current_user
from app.schemas.todo import TodoCreate, TodoUpdate, TodoSingleResponse, TodoListResponse
from app.services import todo as todo_service
from app.utils.errors import format_error_response, NotFoundException, ValidationException

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post(
    "/",
    response_model=TodoSingleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new todo",
    description="Create a new todo for the authenticated user.",
)
def create_todo(
    request: TodoCreate,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new todo for the authenticated user.

    Args:
        request: TodoCreate schema with title and optional description
        user_id: Authenticated user ID from JWT (via dependency)
        session: Database session

    Returns:
        TodoSingleResponse with created todo data

    Security (FR-015, FR-016, FR-024):
        - Requires valid JWT authentication
        - Assigns todo to authenticated user (user_id from JWT, not request)
        - Validates title is non-empty
    """
    try:
        # Create todo for the authenticated user
        created_todo = todo_service.create_todo(
            title=request.title,
            description=request.description,
            user_id=user_id,  # From JWT, not from request body
            priority=request.priority or "medium",
            tags=request.tags,
            session=session
        )

        return TodoSingleResponse(
            success=True,
            data=created_todo,
            error=None
        )

    except ValidationException:
        # Re-raise validation exceptions to be handled by global handler
        raise
    except Exception as e:
        # Error will be handled by global exception handler
        raise


@router.get(
    "/",
    response_model=TodoListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user's todos",
    description="Get all todos for the authenticated user.",
)
def get_todos(
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get all todos for the authenticated user.

    Args:
        user_id: Authenticated user ID from JWT (via dependency)
        session: Database session

    Returns:
        TodoListResponse with list of user's todos

    Security (FR-017, FR-018, FR-019, FR-025):
        - Requires valid JWT authentication
        - Only returns todos owned by authenticated user
        - Orders todos by created_at DESC (newest first)
    """
    try:
        # Get todos for the authenticated user only
        todos = todo_service.get_user_todos(
            user_id=user_id,
            session=session
        )

        return TodoListResponse(
            success=True,
            data=todos,
            error=None
        )

    except Exception as e:
        # Error will be handled by global exception handler
        raise


@router.get(
    "/{id}",
    response_model=TodoSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get specific todo",
    description="Get a specific todo by ID for the authenticated user.",
)
def get_todo(
    id: int,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a specific todo by ID for the authenticated user.

    Args:
        id: Todo ID to retrieve
        user_id: Authenticated user ID from JWT (via dependency)
        session: Database session

    Returns:
        TodoSingleResponse with todo data or 404 if not found/owned

    Security (FR-020, FR-026):
        - Requires valid JWT authentication
        - Only returns todo if it belongs to authenticated user
        - Returns 404 if todo doesn't exist or isn't owned by user
    """
    try:
        # Get the specific todo ensuring it belongs to the user
        todo = todo_service.get_todo_by_id(
            todo_id=id,
            user_id=user_id,
            session=session
        )

        if not todo:
            from app.utils.errors import NotFoundException
            raise NotFoundException(f"Todo with ID {id} not found or not owned by user")

        return TodoSingleResponse(
            success=True,
            data=todo,
            error=None
        )

    except NotFoundException:
        # Re-raise to be handled by global handler
        raise
    except Exception as e:
        # Error will be handled by global exception handler
        raise


@router.patch(
    "/{id}",
    response_model=TodoSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update todo",
    description="Update a specific todo by ID for the authenticated user.",
)
def update_todo(
    id: int,
    request: TodoUpdate,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update a specific todo by ID for the authenticated user.

    Args:
        id: Todo ID to update
        request: TodoUpdate schema with optional fields
        user_id: Authenticated user ID from JWT (via dependency)
        session: Database session

    Returns:
        TodoSingleResponse with updated todo data or 404 if not found/owned

    Security (FR-021, FR-022):
        - Requires valid JWT authentication
        - Only updates todo if it belongs to authenticated user
        - Updates only the fields provided (partial update)
        - Returns 404 if todo doesn't exist or isn't owned by user
    """
    try:
        # Update the specific todo ensuring it belongs to the user
        updated_todo = todo_service.update_todo(
            todo_id=id,
            user_id=user_id,
            session=session,
            title=request.title,
            description=request.description,
            completed=request.completed,
            priority=request.priority,
            tags=request.tags
        )

        if not updated_todo:
            from app.utils.errors import NotFoundException
            raise NotFoundException(f"Todo with ID {id} not found or not owned by user")

        return TodoSingleResponse(
            success=True,
            data=updated_todo,
            error=None
        )

    except ValidationException:
        # Re-raise validation exceptions to be handled by global handler
        raise
    except NotFoundException:
        # Re-raise to be handled by global handler
        raise
    except Exception as e:
        # Error will be handled by global exception handler
        raise


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete todo",
    description="Delete a specific todo by ID for the authenticated user.",
)
def delete_todo(
    id: int,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a specific todo by ID for the authenticated user.

    Args:
        id: Todo ID to delete
        user_id: Authenticated user ID from JWT (via dependency)
        session: Database session

    Returns:
        Success message or 404 if not found/owned

    Security (FR-023):
        - Requires valid JWT authentication
        - Only deletes todo if it belongs to authenticated user
        - Returns 404 if todo doesn't exist or isn't owned by user
    """
    try:
        # Delete the specific todo ensuring it belongs to the user
        success = todo_service.delete_todo(
            todo_id=id,
            user_id=user_id,
            session=session
        )

        if not success:
            from app.utils.errors import NotFoundException
            raise NotFoundException(f"Todo with ID {id} not found or not owned by user")

        return {
            "success": True,
            "data": {"message": f"Todo with ID {id} deleted successfully"},
            "error": None
        }

    except NotFoundException:
        # Re-raise to be handled by global handler
        raise
    except Exception as e:
        # Error will be handled by global exception handler
        raise

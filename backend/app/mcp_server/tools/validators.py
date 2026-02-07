"""Input validation helpers for MCP task tools."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError, field_validator


class AddTaskParams(BaseModel):
    """Parameters for add_task tool."""
    user_id: int
    title: str
    description: Optional[str] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 500:
            raise ValueError('Title must be less than 500 characters')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 10000:
            raise ValueError('Description must be less than 10000 characters')
        return v


class ListTasksParams(BaseModel):
    """Parameters for list_tasks tool."""
    user_id: int
    status: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ['all', 'pending', 'completed']:
            raise ValueError('Status must be one of: all, pending, completed')
        return v


class CompleteTaskParams(BaseModel):
    """Parameters for complete_task tool."""
    user_id: int
    task_id: int


class UpdateTaskParams(BaseModel):
    """Parameters for update_task tool."""
    user_id: int
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('Title cannot be empty')
            if len(v) > 500:
                raise ValueError('Title must be less than 500 characters')
            return v.strip()
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) > 10000:
            raise ValueError('Description must be less than 10000 characters')
        return v


class DeleteTaskParams(BaseModel):
    """Parameters for delete_task tool."""
    user_id: int
    task_id: int


def validate_add_task_params(params: Dict[str, Any]) -> AddTaskParams:
    """Validate parameters for add_task tool."""
    try:
        return AddTaskParams(**params)
    except ValidationError as e:
        raise ValueError(f"Invalid parameters for add_task: {e}")


def validate_list_tasks_params(params: Dict[str, Any]) -> ListTasksParams:
    """Validate parameters for list_tasks tool."""
    try:
        return ListTasksParams(**params)
    except ValidationError as e:
        raise ValueError(f"Invalid parameters for list_tasks: {e}")


def validate_complete_task_params(params: Dict[str, Any]) -> CompleteTaskParams:
    """Validate parameters for complete_task tool."""
    try:
        return CompleteTaskParams(**params)
    except ValidationError as e:
        raise ValueError(f"Invalid parameters for complete_task: {e}")


def validate_update_task_params(params: Dict[str, Any]) -> UpdateTaskParams:
    """Validate parameters for update_task tool."""
    try:
        return UpdateTaskParams(**params)
    except ValidationError as e:
        raise ValueError(f"Invalid parameters for update_task: {e}")


def validate_delete_task_params(params: Dict[str, Any]) -> DeleteTaskParams:
    """Validate parameters for delete_task tool."""
    try:
        return DeleteTaskParams(**params)
    except ValidationError as e:
        raise ValueError(f"Invalid parameters for delete_task: {e}")
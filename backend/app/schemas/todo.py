"""Todo request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TodoCreate(BaseModel):
    """Request model for creating a new todo."""

    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)
    priority: Optional[str] = Field(default="medium", pattern="^(low|medium|high)$")
    tags: Optional[str] = Field(default=None, max_length=500)  # Comma-separated


class TodoUpdate(BaseModel):
    """Request model for updating a todo (all fields optional for PATCH)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    tags: Optional[str] = Field(default=None, max_length=500)


class TodoResponse(BaseModel):
    """Response model for todo data."""

    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility


class TodoSingleResponse(BaseModel):
    """Response wrapper for single todo."""

    success: bool = True
    data: TodoResponse
    error: Optional[dict] = None


class TodoListResponse(BaseModel):
    """Response model for list of todos."""

    success: bool = True
    data: list[TodoResponse]
    error: Optional[dict] = None

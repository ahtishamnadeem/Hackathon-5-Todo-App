"""User database model."""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .todo import Todo
    from .conversation import Conversation


class User(SQLModel, table=True):
    """Database model for User entity.

    Represents a registered user account with authentication credentials.
    Each user owns zero or more todos and can only access their own data.
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships to owned data
    todos: List["Todo"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2026-01-08T10:00:00Z",
                "updated_at": "2026-01-08T10:00:00Z"
            }
        }

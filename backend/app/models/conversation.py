from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class ConversationBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    user_id: int = Field(foreign_key="users.id", nullable=False)


class Conversation(ConversationBase, table=True):
    """
    Represents a user's chat session with the AI assistant, containing metadata
    and linking to associated messages
    """
    __tablename__ = "conversations"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship to user who owns this conversation
    user: "User" = Relationship(back_populates="conversations")

    # Relationship to messages in this conversation
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation"""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading conversation data"""
    id: int
    created_at: datetime
    updated_at: datetime
from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(nullable=False)  # "user", "assistant", or "system"
    content: str = Field(nullable=False)


class Message(MessageBase, table=True):
    """
    Represents individual exchanges between user and AI, including role (user/assistant),
    content, and timestamp
    """
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship to conversation this message belongs to
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class MessageRead(MessageBase):
    """Schema for reading message data"""
    id: int
    timestamp: datetime
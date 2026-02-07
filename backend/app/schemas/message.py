from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    conversation_id: int
    role: str  # "user", "assistant", or "system"
    content: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    timestamp: datetime


class MessageUpdate(BaseModel):
    content: Optional[str] = None
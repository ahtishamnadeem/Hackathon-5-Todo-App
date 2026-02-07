from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .message import MessageRead


class ConversationBase(BaseModel):
    title: Optional[str] = None
    user_id: int


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageRead] = []


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
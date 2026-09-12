from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class ChatBotSessionBase(BaseModel):
    current_state: str
    current_intent: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatBotSessionCreate(ChatBotSessionBase):
    customer_id: int


class ChatBotSessionUpdate(BaseModel):
    current_state: Optional[str] = None
    current_intent: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    is_active: Optional[int] = None


class ChatBotSessionResponse(ChatBotSessionBase):
    session_id: int
    customer_id: int
    is_active: int
    updated_at: datetime

    class Config:
        from_attributes = True

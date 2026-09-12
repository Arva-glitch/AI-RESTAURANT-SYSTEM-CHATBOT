from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ChatBotConversationBase(BaseModel):
    customer_id: int
    user_message: str
    bot_response: str
    detected_intent: Optional[str] = None


class ChatBotConversationCreate(ChatBotConversationBase):
    pass


class ChatBotConversationUpdate(BaseModel):
    bot_response: Optional[str] = None
    detected_intent: Optional[str] = None


class ChatBotConversationResponse(ChatBotConversationBase):
    conversation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

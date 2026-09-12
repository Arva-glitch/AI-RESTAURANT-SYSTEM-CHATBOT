from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Time
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ChatBotConversation(Base):
    __tablename__ = "chatbot_conversations"

    conversation_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    user_message = Column(
        String(1000),
        nullable=False
    )

    bot_response = Column(
        String(2000),
        nullable=False
    )

    detected_intent = Column(
        String(100)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    message_id = Column(Integer)
    sender = Column(Enum('User', 'Bot'))
    response_time_ms = Column(Time)
    message_timestamp = Column(DateTime)
    session_id = Column(String(50))

    customer = relationship(
        "Customer",
        back_populates="conversations"
    )

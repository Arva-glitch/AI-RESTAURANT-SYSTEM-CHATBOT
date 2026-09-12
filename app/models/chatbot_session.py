from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    JSON
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ChatBotSession(Base):
    __tablename__ = "chatbot_sessions"

    session_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    current_state = Column(
        String(50),
        nullable=False,
        default="START"
    )

    current_intent = Column(
        String(50),
        nullable=True
    )

    context = Column(
        JSON,
        nullable=True
    )

    is_active = Column(
        Integer,
        default=1
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="sessions"
    )

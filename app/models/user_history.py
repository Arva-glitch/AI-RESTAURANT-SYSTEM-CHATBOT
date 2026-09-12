from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserHistory(Base):
    __tablename__ = "user_history"

    history_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    activity = Column(
        String(255),
        nullable=False
    )

    activity_type = Column(
        String(50)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="histories"
    )

    # ismai aur entities u can add

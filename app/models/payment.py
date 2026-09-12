from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    String,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    bill_id = Column(
        Integer,
        ForeignKey("bills.bill_id"),
        nullable=False,
        unique=True
    )

    payment_method = Column(String(30))

    payment_status = Column(
        String(30),
        default="Pending"
    )

    transaction_id = Column(
        String(100),
        unique=True
    )

    amount_paid = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_date = Column(
        DateTime,
        server_default=func.now()
    )

    bill = relationship(
        "Bill",
        back_populates="payment"
    )

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurantdescriptions.restaurant_id"
        ),
        nullable=False
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    rating = Column(Integer)

    review_text = Column(String(500))

    review_date = Column(
        DateTime,
        server_default=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="reviews"
    )

    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="reviews"
    )

    order = relationship(
        "Order", back_populates="review")

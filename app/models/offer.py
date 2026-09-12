from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship

from app.database import Base


class Offer(Base):
    __tablename__ = "offers"

    offer_id = Column(Integer, primary_key=True,
                      index=True, autoincrement=True)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurantdescriptions.restaurant_id"),
        nullable=False
    )

    offer_name = Column(String(100))

    description = Column(String(255))

    discount_percentage = Column(Float)

    start_date = Column(Date)

    end_date = Column(Date)

    discount_type = Column(Enum("Percentage", "Flat"))

    minimum_order = Column(DECIMAL(10, 2))

    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="offers"
    )

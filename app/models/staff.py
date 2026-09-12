
from sqlalchemy import Column, Integer, Float, String, Date, DATETIME, Time, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Staff(Base):
    __tablename__ = "staffs"
    staff_id = Column(Integer, primary_key=True,
                      index=True, autoincrement=True)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurantdescriptions.restaurant_id"),
        nullable=False
    )

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    phone_number = Column(String(15))
    email = Column(String(100))
    role = Column(String(50))
    salary = Column(Integer)
    shift = Column(String(30))
    joining_date = Column(Date)
    resigning_date = Column(Date)

    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="staff_members"
    )

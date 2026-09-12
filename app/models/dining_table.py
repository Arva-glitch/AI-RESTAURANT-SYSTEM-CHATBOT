from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Diningtable(Base):
    __tablename__ = "diningtables"

    table_id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(10), nullable=False, unique=True)
    seating_capacity = Column(Integer, nullable=False)
    table_type = Column(String(30))
    table_status = Column(String(30), default="Available")
    floor_number = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="table")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base


class Address(Base):
    __tablename__ = "addresses"
    address_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )
    address_line1 = Column(String(300), nullable=False)
    address_line2 = Column(String(255))
    landmark = Column(String(300))
    pincode = Column(String(20), nullable=False)
    address_type = Column(String(20))
# Relationship
    customer = relationship(
        "Customer",
        back_populates="addresses"
    )

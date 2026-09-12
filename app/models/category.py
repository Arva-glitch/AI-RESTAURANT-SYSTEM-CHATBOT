from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)

    category_name = Column(String(100), nullable=False)

    description = Column(String(255))

    menu_items = relationship("Menu", back_populates="category")

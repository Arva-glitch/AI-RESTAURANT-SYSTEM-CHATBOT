from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CustomerFavourite(Base):
    __tablename__ = "customer_favourites"

    favourite_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    menu_id = Column(
        Integer,
        ForeignKey("menu.menu_id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="favourites"
    )

    menu = relationship(
        "Menu",
        back_populates="favourites"
    )

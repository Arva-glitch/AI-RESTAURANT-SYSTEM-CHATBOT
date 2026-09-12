from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base
from sqlalchemy.orm import relationship


class Coupon(Base):
    __tablename__ = "coupons"

    coupon_id = Column(Integer, primary_key=True, index=True)

    coupon_code = Column(String(50), unique=True)

    discount_percentage = Column(Float)

    minimum_order_amount = Column(Float)

    expiry_date = Column(Date)

    usage_limit = Column(Integer)

    orders = relationship(
        "Order",
        back_populates="coupon"
    )

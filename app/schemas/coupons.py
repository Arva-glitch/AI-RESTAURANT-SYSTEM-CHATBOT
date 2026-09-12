from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from decimal import Decimal


class CouponBase(BaseModel):
    coupon_code: str
    discount_percentage: Decimal
    minimum_order_amount: Decimal
    expiry_date: date
    usage_limit: int


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    coupon_code: Optional[str] = None
    discount_percentage: Optional[float] = None
    minimum_order_amount: Optional[float] = None
    expiry_date: Optional[date] = None
    usage_limit: Optional[int] = None


class CouponResponse(CouponBase):
    coupon_id: int

    model_config = ConfigDict(from_attributes=True)

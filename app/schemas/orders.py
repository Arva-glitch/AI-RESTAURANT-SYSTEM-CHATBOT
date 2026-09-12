from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional
from app.schemas.enums import OrderStatus, OrderType


class OrderBase(BaseModel):
    customer_id: int

    booking_id: Optional[int] = None

    restaurant_description_id: int

    coupon_id: Optional[int] = None

    order_type: OrderType

    order_status: OrderStatus = OrderStatus.pending

    total_amount: Decimal

    special_instruction: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    coupon_id: Optional[int] = None
    order_status: Optional[str] = None
    total_amount: Optional[Decimal] = None
    special_instruction: Optional[str] = None


class OrderResponse(OrderBase):
    order_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional
from app.schemas.enums import PaymentMethod
from app.schemas.enums import PaymentStatus


class PaymentBase(BaseModel):
    bill_id: int

    payment_method: PaymentMethod

    payment_status: PaymentStatus = PaymentStatus.pending

    transaction_id: Optional[str] = None

    amount_paid: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_method: Optional[str] = None
    payment_status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None
    amount_paid: Optional[Decimal] = None


class PaymentResponse(PaymentBase):
    payment_id: int

    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)

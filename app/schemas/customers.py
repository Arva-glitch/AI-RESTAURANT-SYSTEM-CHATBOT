from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date


class CustomerBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[EmailStr] = None

    gender: Optional[str] = None

# --------Rest API---------------------------------------------------------


class CustomerCreate(CustomerBase):
    pass


# this schema will be used only by register_telegram_customer
class TelegramCustomerCreate(BaseModel):

    telegram_id: int

    username: str | None = None

    first_name: str

    phone: str


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None


class CustomerResponse(CustomerBase):
    customer_id: int
    telegram_id: int | None = None

    username: str | None = None

    total_orders: int
    created_at: date
    total_members: int
    model_config = ConfigDict(from_attributes=True)

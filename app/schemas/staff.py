from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class StaffBase(BaseModel):
    restaurant_description_id: int
    first_name: str
    last_name: Optional[str] = None
    phone_number: str
    email: EmailStr
    role: str
    salary: int
    shift: str


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    salary: Optional[int] = None
    shift: Optional[str] = None


class StaffResponse(StaffBase):
    staff_id: int

    model_config = ConfigDict(from_attributes=True)

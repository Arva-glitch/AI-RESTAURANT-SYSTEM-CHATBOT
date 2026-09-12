from pydantic import BaseModel, ConfigDict
from typing import Optional


class AddressBase(BaseModel):
    customer_id: int
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class AddressResponse(AddressBase):
    address_id: int

    model_config = ConfigDict(from_attributes=True)

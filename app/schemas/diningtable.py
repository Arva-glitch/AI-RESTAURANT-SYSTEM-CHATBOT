from pydantic import BaseModel, ConfigDict
from typing import Optional


class DiningtableBase(BaseModel):
    table_number: str
    seating_capacity: int
    table_type: Optional[str] = None
    table_status: str = "Available"


class DiningtableCreate(DiningtableBase):
    pass


class DiningtableUpdate(BaseModel):
    table_number: Optional[str] = None
    seating_capacity: Optional[int] = None
    table_type: Optional[str] = None
    table_status: Optional[str] = None


class DiningtableResponse(DiningtableBase):
    restaurant_id: int

    model_config = ConfigDict(from_attributes=True)

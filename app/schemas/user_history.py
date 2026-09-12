from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserHistoryBase(BaseModel):
    customer_id: int
    activity: str
    activity_type: Optional[str] = None


class UserHistoryCreate(UserHistoryBase):
    pass


class UserHistoryUpdate(BaseModel):
    activity: Optional[str] = None
    activity_type: Optional[str] = None


class UserHistoryResponse(UserHistoryBase):
    history_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

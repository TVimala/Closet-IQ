from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class NotificationOut(BaseModel):

    id: int
    user_id: str
    notification_type: str
    title: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = None
    scheduled_for: Optional[date] = None
    read: bool
    delivery_status: str

    class Config:
        from_attributes = True

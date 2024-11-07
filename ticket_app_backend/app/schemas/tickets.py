from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class TicketCreate(BaseModel):
    user_id: int
    event_date_id: int
    ticket: int
    check_in: bool = False

class TicketRead(BaseModel):
    id: int
    user_id: int
    event_date_id: int
    ticket: int
    check_in: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    user_id: Optional[int]
    event_date_id: Optional[int]
    ticket: Optional[int]
    check_in: Optional[bool]

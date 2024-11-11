from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from app.schemas.user import UserInTicket

class TicketCreate(BaseModel):
    user_id: int
    event_date_id: int
    check_in: bool = False

class TicketRead(BaseModel):
    id: int
    user_id: int
    event_date_id: int
    ticket_number: int
    check_in: bool
    created_at: datetime
    user: UserInTicket

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    user_id: Optional[int]
    event_date_id: Optional[int]
    ticket_number: Optional[int]
    check_in: Optional[bool]

class TicketCheckInUpdate(BaseModel):
    check_in: Optional[bool]
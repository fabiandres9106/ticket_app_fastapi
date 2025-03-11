from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime
from app.schemas.user import UserInTicket
from app.schemas.event_dates import EventDateInTicket

class TicketCreate(BaseModel):
    user_id: int
    event_date_id: int
    ticket_name: str
    check_in: bool = False

class TicketRead(BaseModel):
    id: int
    user_id: int
    event_date_id: int
    ticket_name: str
    ticket_number: int
    check_in: bool
    created_at: datetime
    user: Optional[UserInTicket]  # Asegúrate de que el modelo Ticket tiene la relación definida con User
    event_date: Optional[EventDateInTicket]  # Asegúrate de que el modelo Ticket tiene la relación definida con EventDate

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    user_id: Optional[int]
    event_date_id: Optional[int]
    ticket_name: Optional[str]
    ticket_number: Optional[int]
    check_in: Optional[bool]

class TicketCheckInUpdate(BaseModel):
    check_in: Optional[bool]
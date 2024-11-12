from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from app.schemas.stage import StageInEventDate  

class EventDateCreate(BaseModel):
    event_id: int
    date_time: datetime
    available_tickets: int

class EventDateRead(BaseModel):
    id: int
    event_id: int
    date_time: datetime
    available_tickets: int
    created_at: datetime
    tickets_reserved: int  
    tickets_not_reserved: int  
    tickets_checkin: int  

    class Config:
        from_attributes = True

class EventDateUpdate(BaseModel):
    event_id: Optional[int]
    date_time: Optional[datetime]
    available_tickets: Optional[int]


class EventDateInTicket(BaseModel):
    id: int
    event_id: Optional[int] = None
    date_time: Optional[datetime] = None
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_artistic_team: Optional[Any] = None
    stage: Optional[StageInEventDate] = None  # Información del Stage

    class Config:
        from_attributes = True
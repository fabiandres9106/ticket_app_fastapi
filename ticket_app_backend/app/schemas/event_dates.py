from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

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

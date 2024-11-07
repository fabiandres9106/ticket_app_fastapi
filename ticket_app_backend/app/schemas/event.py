from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class EventCreate(BaseModel):
    event_name: str
    stage_id: int
    user_id: int
    pulep: Optional[str] = None
    description: Optional[str] = None
    artistic_team: Optional[Any] = None
    active: bool = True

class EventRead(BaseModel):
    id: int
    event_name: str
    stage_id: int
    user_id: int
    pulep: Optional[str]
    description: Optional[str]
    artistic_team: Optional[Any]
    created_at: datetime
    active: bool

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    event_name: Optional[str]
    stage_id: Optional[int]
    user_id: Optional[int]
    pulep: Optional[str]
    description: Optional[str]
    artistic_team: Optional[Any]
    active: bool

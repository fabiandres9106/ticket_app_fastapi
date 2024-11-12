from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class StageCreate(BaseModel):
    stage_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    social_media: Optional[Any] = None
    contact_name: Optional[str] = None
    capacity: int
    city: Optional[str] = None
    departament: Optional[str]
    user_id: int

class StageRead(BaseModel):
    id: int
    stage_name: str
    address: Optional[str]
    phone: Optional[str]
    social_media: Optional[Any]
    contact_name: Optional[str]
    capacity: int
    city: Optional[str]
    departament: Optional[str]
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class StageUpdate(BaseModel):
    stage_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    social_media: Optional[Any]
    contact_name: Optional[str]
    capacity: Optional[str]
    city: Optional[str]
    departament: Optional[str]
    user_id: Optional[int]

class StageInEventDate(BaseModel):
    id: int
    stage_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
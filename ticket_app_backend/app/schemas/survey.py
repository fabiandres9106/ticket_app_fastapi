from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class SurveyCreate(BaseModel):
    user_id: int
    age: Optional[str] = None
    genere: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    relationship_theatre: Optional[str] = None
    motivations: Optional[Any] = None
    others_motivations: Optional[str] = None
    information_medium: Optional[str] = None
    other_events: Optional[Any] = None
    permision_research: bool = True

class SurveyRead(BaseModel):
    id: int
    user_id: int
    age: Optional[str]
    genere: Optional[str]
    education: Optional[str]
    occupation: Optional[str]
    relationship_theatre: Optional[str]
    motivations: Optional[Any]
    others_motivations: Optional[str]
    information_medium: Optional[str]
    other_events: Optional[Any]
    permision_research: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SurveyUpdate(BaseModel):
    user_id: int
    age: Optional[str]
    genere: Optional[str]
    education: Optional[str]
    occupation: Optional[str]
    relationship_theatre: Optional[str]
    motivations: Optional[Any]
    others_motivations: Optional[str]
    information_medium: Optional[str]
    other_events: Optional[Any]
    permision_research: bool

from sqlalchemy import func, ForeignKey, Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime
from app.db.base import Base
from pydantic import BaseModel

from app.models.stage import Stage
from app.models.user import User
#from app.models.event_dates import EventDate

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(255), nullable=False)
    stage_id = Column(Integer(), ForeignKey("stages.id"), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    pulep = Column(String(10), nullable=True)
    description = Column(String(255), nullable=True)
    artistic_team = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    active = Column(Boolean, default=True)

    stage = relationship('Stage', back_populates="event")
    user = relationship('User')
    event_dates = relationship("EventDate", back_populates="event")
from sqlalchemy import func, ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime
from app.db.base import Base

from app.models.event import Event

class EventDate(Base):
    __tablename__ = "event_dates"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer(), ForeignKey("events.id"), nullable=False)
    date_time = Column(DateTime(), nullable=False)
    available_tickets = Column(Integer())
    created_at = Column(DateTime, server_default=func.now())

    event = relationship('Event')
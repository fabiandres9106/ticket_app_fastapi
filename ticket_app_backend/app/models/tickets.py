from sqlalchemy import func, ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime
from app.db.base import Base
from pydantic import BaseModel

from app.models.user import User
from app.models.event_dates import EventDate

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    event_date_id = Column(Integer(), ForeignKey("event_dates.id"), nullable=False)
    ticket = Column(Integer())
    check_in = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship('User')
    event_date = relationship('EventDate')
from sqlalchemy import func, ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Session

from datetime import datetime
from app.db.base import Base
from pydantic import BaseModel

import random

from app.models.user import User
#from app.models.event_dates import EventDate

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    event_date_id = Column(Integer(), ForeignKey("event_dates.id"), nullable=False)
    ticket_number = Column(Integer())
    check_in = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship('User')
    event_date = relationship("EventDate", back_populates="tickets")

    def generate_unique_ticket_number(self, db: Session):
        """Genera un número de ticket único."""
        while True:
            ticket_number = random.randint(100000, 999999)
            existing_ticket = db.query(Ticket).filter(Ticket.ticket_number == ticket_number).first()
            if not existing_ticket:
                return ticket_number
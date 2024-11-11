from sqlalchemy import func, ForeignKey, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship, Session

from datetime import datetime
from app.db.base import Base

from app.models.event import Event
from app.models.tickets import Ticket 

class EventDate(Base):
    __tablename__ = "event_dates"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer(), ForeignKey("events.id"), nullable=False)
    date_time = Column(DateTime(), nullable=False)
    available_tickets = Column(Integer())
    created_at = Column(DateTime, server_default=func.now())

    event = relationship("Event", back_populates="event_dates")
    tickets = relationship("Ticket", back_populates="event_date")

    # Funciones para consultas de tickets
    def tickets_not_reserved(self, db: Session) -> int:
        """Retorna la cantidad de tickets no reservados."""
        reserved_tickets = db.query(Ticket).filter(Ticket.event_date_id == self.id).count()
        return self.available_tickets - reserved_tickets

    def tickets_reserved(self, db: Session) -> int:
        """Retorna la cantidad de tickets reservados."""
        return db.query(Ticket).filter(Ticket.event_date_id == self.id).count()

    def tickets_checkin(self, db: Session) -> int:
        """Retorna la cantidad de tickets que han hecho check-in."""
        checkin_tickets = db.query(Ticket).filter(Ticket.event_date_id == self.id, Ticket.check_in == True).count()
        return checkin_tickets
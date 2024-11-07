from sqlalchemy.orm import Session
from app.models.event_dates import EventDate
from app.schemas.event_dates import EventDateCreate, EventDateUpdate
from typing import Optional, List

def create_event_date(db: Session, event_date: EventDateCreate) -> EventDate:
    """Crea un nuevo EventDate en BD"""
    db_event_date = EventDate(
        event_id = event_date.event_id,
        date_time = event_date.date_time,
        available_tickets = event_date.available_tickets
    )
    db.add(db_event_date)
    db.commit()
    db.refresh(db_event_date)
    return db_event_date

def get_event_date(db: Session, event_date_id: int) -> Optional[EventDate]:
    """Obtiene un event_date por ID"""
    return db.query(EventDate).filter(EventDate.id == event_date_id).first()

def get_event_dates(db: Session, skip: int = 0, limit: int = 10) -> List[EventDate]:
    """Obtiene una lista de event_date con paginación"""
    return db.query(EventDate).offset(skip).limit(limit).all()

def update_event_date(db: Session, event_date_id: int, event_date_update: EventDateUpdate) -> Optional[EventDate]:
    """Actualiza un event_date existente"""
    db_event_date = db.query(EventDate).filter(EventDate.id == event_date_id).first()
    if db_event_date is None:
        return None
    for key, value in event_date_update.model_dump(exclude_unset=True).items():
        setattr(db_event_date, key, value)
    db.commit()
    db.refresh(db_event_date)
    return db_event_date

def delete_event_date(db: Session, event_date_id: int) -> bool:
    """Elimina un event_date por ID"""
    db_event_date = db.query(EventDate).filter(EventDate.id == event_date_id).first()
    if db_event_date is None:
        return False
    db.delete(db_event_date)
    db.commit()
    return True
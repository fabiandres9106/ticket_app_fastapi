from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from typing import Optional, List

def create_event(db: Session, event: EventCreate) -> Event:
    """Crea un nuevo Event en BD"""
    db_event = Event(
        event_name = event.event_name,
        stage_id = event.stage_id,
        user_id = event.user_id,
        pulep = event.pulep,
        description = event.description,
        artistic_team = event.artistic_team,
        active = event.active
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int) -> Optional[Event]:
    """Obtiene un Event por ID"""
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 10) -> List[Event]:
    """Obtiene una lista de Event con paginación"""
    return db.query(Event).offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Optional[Event]:
    """Actualiza un Event existente"""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        return None
    for key, value in event_update.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    """Elimina un Event por ID"""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        return False
    db.delete(db_event)
    db.commit()
    return True
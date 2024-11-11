from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.event import create_event, get_event, get_events, update_event, delete_event
from app.crud.event_dates import get_event_dates_by_event_id

from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.schemas.event_dates import EventDateRead

from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=EventRead)
def create_event_endpoint(event: EventCreate, db: Session = Depends(get_db)):
    db_event = create_event(db=db, event=event)
    return db_event

@router.get("/{event_id}", response_model=EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = get_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.get("/{event_id}/event_dates", response_model=List[EventDateRead])
def read_event_dates(event_id: int, db: Session = Depends(get_db)):
    event_dates = get_event_dates_by_event_id(db, event_id=event_id)
    if not event_dates:
        raise HTTPException(status_code=404, detail="No dates found for the event.")
    return event_dates

@router.get("/", response_model=List[EventRead])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_events(db=db, skip=skip, limit=limit)

@router.put("/{event_id}", response_model=EventRead)
def update_event_endpoint(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    db_event = update_event(db=db, event_id=event_id, event_update=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.delete("/{event_id}", response_model=bool)
def delete_event_endpoint(event_id: int, db: Session = Depends(get_db)):
    success = delete_event(db=db, event_id=event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return success
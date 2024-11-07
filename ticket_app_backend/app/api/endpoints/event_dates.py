from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.event_dates import create_event_date, get_event_date, get_event_dates, update_event_date, delete_event_date
from app.schemas.event_dates import EventDateCreate, EventDateRead, EventDateUpdate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=EventDateRead)
def create_event_date_endpoint(event_date: EventDateCreate, db: Session = Depends(get_db)):
    db_event_date = create_event_date(db=db, event_date=event_date)
    return db_event_date

@router.get("/{event_date_id}", response_model=EventDateRead)
def read_event_date(event_date_id: int, db: Session = Depends(get_db)):
    db_event_date = get_event_date(db=db, event_date_id=event_date_id)
    if db_event_date is None:
        raise HTTPException(status_code=404, detail="EventDate not found")
    return db_event_date

@router.get("/", response_model=List[EventDateRead])
def read_event_dates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_event_dates(db=db, skip=skip, limit=limit)

@router.put("/{event_date_id}", response_model=EventDateRead)
def update_event_date_endpoint(event_date_id: int, event_date: EventDateUpdate, db: Session = Depends(get_db)):
    db_event_date = update_event_date(db=db, event_date_id=event_date_id, event_date_update=event_date)
    if db_event_date is None:
        raise HTTPException(status_code=404, detail="EventDate not found")
    return db_event_date

@router.delete("/{event_date_id}", response_model=bool)
def delete_event_date_endpoint(event_date_id: int, db: Session = Depends(get_db)):
    success = delete_event_date(db=db, event_date_id=event_date_id)
    if not success:
        raise HTTPException(status_code=404, detail="EventDate not found")
    return success
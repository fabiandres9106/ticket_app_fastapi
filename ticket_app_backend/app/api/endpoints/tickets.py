from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.tickets import create_ticket, get_ticket, get_tickets, update_ticket, delete_ticket
from app.schemas.tickets import TicketCreate, TicketRead, TicketUpdate, TicketCheckInUpdate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=TicketRead)
def create_ticket_endpoint(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = create_ticket(db=db, ticket=ticket)
    return db_ticket

@router.get("/{ticket_id}", response_model=TicketRead)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = get_ticket(db=db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.get("/", response_model=List[TicketRead])
def read_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_tickets(db=db, skip=skip, limit=limit)

@router.put("/{ticket_id}", response_model=TicketRead)
def update_ticket_endpoint(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = update_ticket(db=db, ticket_id=ticket_id, ticket_update=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket_endpoint(ticket_id: int, ticket: TicketCheckInUpdate, db: Session = Depends(get_db)):
    print("Received data:", ticket.model_dump())  # Log de los datos recibidos
    db_ticket = update_ticket(db=db, ticket_id=ticket_id, ticket_update=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.delete("/{ticket_id}", response_model=bool)
def delete_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
    success = delete_ticket(db=db, ticket_id=ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return success
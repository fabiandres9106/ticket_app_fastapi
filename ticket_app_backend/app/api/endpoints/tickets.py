from fastapi import APIRouter, Depends, HTTPException
from fastapi import BackgroundTasks
from app.email.email_utils import send_confirmation_email
from sqlalchemy.orm import Session
from typing import List

from app.crud.tickets import create_ticket, get_ticket, get_tickets, update_ticket, delete_ticket
from app.schemas.tickets import TicketCreate, TicketRead, TicketUpdate, TicketCheckInUpdate
from app.db.session import get_db

from app.models.tickets import Ticket

router = APIRouter()

@router.post("/", response_model=TicketRead)
def create_ticket_endpoint(ticket: TicketCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()):
    # Crear el ticket en la base de datos
    db_ticket = create_ticket(db=db, ticket=ticket)
    
    # Volver a consultar el ticket para cargar las relaciones con user y event_date
    db_ticket_with_relations = db.query(Ticket).filter(Ticket.id == db_ticket.id).first()

    if db_ticket_with_relations and db_ticket_with_relations.user:
        event_datetime = db_ticket_with_relations.event_date.date_time
        formatted_date = event_datetime.strftime("%d-%m-%Y")  # Formato de fecha
        formatted_time = event_datetime.strftime("%I:%M %p")  # Formato de hora con AM/PM

        # Preparar la información del ticket para el correo
        ticket_info = {
            "ticket_number": db_ticket_with_relations.ticket_number,
            "ticket_name": db_ticket_with_relations.ticket_name,
            "event_date": formatted_date,
            "event_time": formatted_time,
            "event_name": db_ticket_with_relations.event_date.event.event_name,
            "stage_name": db_ticket_with_relations.event_date.event.stage.stage_name,
            "stage_address": db_ticket_with_relations.event_date.event.stage.address
        }
        
        # Añadir la tarea de enviar el correo electrónico en segundo plano
        background_tasks.add_task(
            send_confirmation_email,  # función a ejecutar
            email_to=db_ticket_with_relations.user.email,
            ticket_info=ticket_info,
            attachment_path=f"flyer_witches.jpg"
        )
    
    return db_ticket_with_relations

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
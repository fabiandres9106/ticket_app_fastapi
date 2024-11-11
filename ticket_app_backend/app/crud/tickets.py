from sqlalchemy.orm import Session
from app.models.tickets import Ticket
from app.schemas.tickets import TicketCreate, TicketUpdate
from typing import Optional, List

def create_ticket(db: Session, ticket: TicketCreate) -> Ticket:
    """Crea un nuevo Ticket en BD"""
    db_ticket = Ticket(
        user_id = ticket.user_id,
        event_date_id = ticket.event_date_id,
        check_in = ticket.check_in,
    )

    # Generar el ticket_number único si aún no existe
    if db_ticket.ticket_number is None:
        db_ticket.ticket_number = db_ticket.generate_unique_ticket_number(db)

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int):
    """Obtiene un Ticket por ID"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket:
        user = ticket.user  # Aquí accedes al usuario relacionado
        return {
            "ticket_id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "user_id": user.id,
            "user_email": user.email,
            "user_name": user.name,
            "checkin": ticket.check_in,
            "event_date_id": ticket.event_date_id
            # Otros campos del usuario si los necesitas
        }
    return None

def get_tickets(db: Session, skip: int = 0, limit: int = 10) -> List[Ticket]:
    """Obtiene una lista de Ticket con paginación"""
    return db.query(Ticket).offset(skip).limit(limit).all()

def update_ticket(db: Session, ticket_id: int, ticket_update: TicketUpdate) -> Optional[Ticket]:
    """Actualiza un Ticket existente"""
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        return None
    for key, value in ticket_update.model_dump(exclude_unset=True).items():
        setattr(db_ticket, key, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int) -> bool:
    """Elimina un Ticket por ID"""
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        return False
    db.delete(db_ticket)
    db.commit()
    return True
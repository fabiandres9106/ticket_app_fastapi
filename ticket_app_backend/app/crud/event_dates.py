from sqlalchemy.orm import Session
from app.models.event_dates import EventDate
from app.models.tickets import Ticket
from app.schemas.event_dates import EventDateCreate, EventDateUpdate, EventDateRead
from app.schemas.tickets import TicketRead
from app.schemas.user import UserInTicket
from app.schemas.event_dates import EventDateInTicket
from app.schemas.stage import StageInEventDate  
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

def get_event_date(db: Session, event_date_id: int) -> Optional[EventDateRead]:
    """Obtiene un event_date por ID y calcula los tickets reservados, no reservados y check-in"""
    event_date = db.query(EventDate).filter(EventDate.id == event_date_id).first()
    
    if event_date:
        # Usar los métodos para calcular los valores de tickets
        return EventDateRead(
            id=event_date.id,
            event_id=event_date.event_id,
            date_time=event_date.date_time,
            available_tickets=event_date.available_tickets,
            created_at=event_date.created_at,
            tickets_reserved=event_date.tickets_reserved(db),  
            tickets_not_reserved=event_date.tickets_not_reserved(db),  
            tickets_checkin=event_date.tickets_checkin(db)
        )
    
    return None

def get_event_dates(db: Session, skip: int = 0, limit: int = 10) -> List[EventDate]:
    """Obtiene una lista de event_date con paginación"""
    return db.query(EventDate).offset(skip).limit(limit).all()

def get_event_dates_by_event_id(db: Session, event_id: int) -> List[EventDateRead]:
    event_dates = db.query(EventDate).filter(EventDate.event_id == event_id).all()
    
    # Construimos la respuesta con los métodos del modelo
    event_dates_response = []
    for event_date in event_dates:
        event_dates_response.append(EventDateRead(
            id=event_date.id,
            event_id=event_date.event_id,
            date_time=event_date.date_time,
            available_tickets=event_date.available_tickets,
            created_at=event_date.created_at,
            tickets_reserved=event_date.tickets_reserved(db),  
            tickets_not_reserved=event_date.tickets_not_reserved(db),  
            tickets_checkin=event_date.tickets_checkin(db) 
        ))
    
    return event_dates_response

def get_event_dates_tickets(db: Session, event_date_id: int) -> List[TicketRead]:
    event_dates_tickets = db.query(Ticket).filter(Ticket.event_date_id == event_date_id).all()
    
    # Construimos la respuesta con los métodos del modelo
    event_dates_tickets_response = []
    for ticket in event_dates_tickets:
        user = ticket.user
        ticket_name = ticket.ticket_name
        event_date = ticket.event_date  # Cargar la relación event_date
        event = event_date.event  # Cargar la relación event para obtener el nombre del evento
        stage = event.stage 

        # Crear una instancia de UserInTicket a partir del usuario
        user_data = UserInTicket(
            id=user.id,
            name=user.name,
            email=user.email
        )

        # Crear una instancia de StageInEventDate para incluirla en EventDateInTicket
        stage_data = StageInEventDate(
            id=stage.id,
            stage_name=stage.stage_name,
            address=stage.address,
            city=stage.city
        )

        # Crear una instancia de EventDateInTicket con el nombre del evento
        event_date_data = EventDateInTicket(
            id=event_date.id,
            event_id=event_date.event_id,
            date_time=event_date.date_time,
            event_name=event.event_name,  # Incluye el nombre del evento
            event_description = event.description,
            event_artistic_team = event.artistic_team,
            stage=stage_data  # Incluye la información del Stage
        )

        event_dates_tickets_response.append(TicketRead(
            id=ticket.id,
            user_id=ticket.user_id,
            ticket_name=ticket.ticket_name,
            event_date_id=ticket.event_date_id,
            ticket_number=ticket.ticket_number,
            check_in=ticket.check_in,
            created_at=ticket.created_at,
            user=user_data,  # Usar la instancia UserInTicket
            event_date=event_date_data  # Usar la instancia EventDateInTicket con el nombre del evento
        ))
    
    return event_dates_tickets_response

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
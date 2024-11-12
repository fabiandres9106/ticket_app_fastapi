from app.email.email_utils import send_survey_email  # Ajusta esto a la función correcta de envío de correo
from app.crud.event_dates import get_event_dates  # Asegúrate de que tienes la función correcta
from app.crud.tickets import get_tickets_by_event_data
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db  # Importa get_db
import asyncio

async def schedule_emails_for_events():
    db = next(get_db())  # Obtén la sesión de la base de datos sin usar async
    event_dates = get_event_dates(db)  # No uses `await` aquí si devuelve una lista
    now = datetime.now()

    for event_date in event_dates:
        send_time = event_date.date_time + timedelta(hours=2)
        #send_time = now + timedelta(seconds=10)
        delay = (send_time - now).total_seconds()
        if delay > 0:
            tickets = get_tickets_by_event_data(db, event_date.id)
            for ticket in tickets:
                ticket_email = ticket.user.email

                event_datetime = ticket.event_date.date_time
                formatted_date = event_datetime.strftime("%d-%m-%Y")  # Formato de fecha
                formatted_time = event_datetime.strftime("%I:%M %p")  # Formato de hora con AM/PM

                ticket_info = {
                    "ticket_number": ticket.ticket_number,
                    "ticket_name": ticket.ticket_name,
                    "event_date": formatted_date,
                    "event_time": formatted_time,
                    "event_name": ticket.event_date.event.event_name,
                    "stage_name": ticket.event_date.event.stage.stage_name,
                    "stage_address": ticket.event_date.event.stage.address
                }
                asyncio.create_task(delayed_email(event_date.id, delay, ticket_email, ticket_info))

async def delayed_email(event_date_id: int, delay: float, ticket_email: str, ticket_info: dict):
    await asyncio.sleep(delay)
    # Lógica para enviar el email    
    await send_survey_email(ticket_email, ticket_info) 
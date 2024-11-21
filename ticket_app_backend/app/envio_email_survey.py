from sqlalchemy.orm import Session
from datetime import datetime

from app.models.tickets import Ticket

from app.email.email_utils import send_survey_email

from app.db.session import SessionLocal, engine

import asyncio


def emails_for_survey(db: Session) -> None:
    tickets = db.query(Ticket).filter(Ticket.check_in == True).all()

    
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

        asyncio.run(send_survey_email(ticket_email, ticket_info)) 

        print(f"Email Survey enviado a: {ticket_email}")
    '''
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
    '''

if __name__ == "__main__":
    db = SessionLocal()
    try:
        emails_for_survey(db)
    finally:
        db.close()

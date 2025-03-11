import csv
import asyncio
import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi import BackgroundTasks
from typing import List
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from app.db.session import get_db

from app.models.tickets import Ticket
from app.models.survey import Survey
from app.models.user import User
from app.models.event_dates import EventDate

from app.schemas.tickets import TicketRead
from app.schemas.event_dates import EventDateRead
from app.schemas.user import UserRead, UserInTicket
from app.schemas.survey import SurveyRead

from app.crud.tickets import get_tickets
from app.crud.user import get_users  # Asume que existe la función get_user_by_email
from app.crud.survey import get_surveys

router = APIRouter()

@router.get("/")
# Cargar los datos del archivo CSV
def create_csv(db: Session = Depends(get_db)):
    tickets = get_tickets(db=db)
    users = get_users(db=db)
    survey = get_surveys(db=db)

    tickets_with_data = [
        TicketRead(
            id=ticket.id,
            user_id=ticket.user_id,
            
            user=[UserInTicket(
                id=user_in_ticket.id, 
                name=user_in_ticket.name, 
                email=user_in_ticket.email,
                city=user_in_ticket.city,
                localidad=user_in_ticket.localidad,
                municipio_aledano=user_in_ticket.municipio_aledano,
                ) 
                for user_in_ticket in ticket.user],
            event_date_id=ticket.event_date_id,
            ticket_number=ticket.ticket_number,
            ticket_name=ticket.ticket_name,
            event_date=ticket.event_date,
            check_in=ticket.check_in,
            created_at=ticket.created_at
        )
        for ticket in tickets
    ]
    return tickets_with_data

@router.get("/download_csv", response_class=FileResponse)
def download_csv(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    users = db.query(User).all()
    surveys = db.query(Survey).all()
    event_dates = db.query(EventDate).all()

    # Ruta del archivo CSV
    current_directory = os.path.dirname(os.path.abspath(__file__))  # app/email
    static_directory = os.path.abspath(os.path.join(current_directory, "../../static"))
    
    # Crear el directorio si no existe
    if not os.path.exists(static_directory):
        os.makedirs(static_directory)
    
    # Generar el nombre del archivo con la fecha y hora actual
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{current_datetime}_tickets_data.csv"
    file_path = os.path.join(static_directory, file_name)

    # Crear el archivo CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Ticket Number", "Ticket Name", "User ID", "User Name", "User Email", 
            "User City", "User Localidad", "User Municipio Aledano", "Survey Age", 
            "Survey Genere", "Survey Education", "Survey Occupation", 
            "Survey Relationship Theatre", "Survey Motivations", 
            "Survey Others Motivations", "Survey Information Medium", 
            "Survey Other Events", "Survey Permission Research", "Check-In",
            "Event Date"
        ])

        for ticket in tickets:
            user = next((u for u in users if u.id == ticket.user_id), None)
            survey = next((s for s in surveys if s.user_id == ticket.user_id), None)
            event_date = next((e for e in event_dates if e.id == ticket.event_date_id), None)
            writer.writerow([
                ticket.ticket_number, ticket.ticket_name, ticket.user_id, 
                user.name if user else None, user.email if user else None, 
                user.city if user else None, user.localidad if user else None, 
                user.municipio_aledano if user else None, survey.age if survey else None, 
                survey.genere if survey else None, survey.education if survey else None, 
                survey.occupation if survey else None, survey.relationship_theatre if survey else None, 
                survey.motivations if survey else None, survey.others_motivations if survey else None, 
                survey.information_medium if survey else None, survey.other_events if survey else None, 
                survey.permision_research if survey else None, ticket.check_in,
                event_date.date_time.strftime("%Y-%m-%d %H:%M:%S") if event_date else None
            ])

    return file_path

# Ruta del archivo CSV
current_directory = os.path.dirname(os.path.abspath(__file__))  # app/email
static_directory = os.path.abspath(os.path.join(current_directory, "../../static"))
file_path = os.path.join(static_directory, "bwitches_database6_converted.csv")
print(file_path)

import csv
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import create_user, get_user_by_email  # Asume que existe la función get_user_by_email
from app.crud.tickets import create_ticket
from app.crud.survey import create_survey
from app.schemas.user import UserCreate
from app.schemas.tickets import TicketCreate
from app.schemas.survey import SurveyCreate
from app.models.tickets import Ticket
from app.email.email_utils import send_confirmation_email
import asyncio
import os

# Cargar los datos del archivo CSV
def load_data_from_csv(file_path: str):
    db: Session = next(get_db())  # Crear una sesión de base de datos

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Verificar si el usuario ya existe por su email
            existing_user = get_user_by_email(db, email=row['email'])
            if existing_user:
                user = existing_user
            else:
                # Crear usuario si no existe
                user_data = UserCreate(
                    email=row['email'],
                    username=row.get('username'),
                    password=row['email'],  # Cambiar por lógica de generación de contraseña
                    name=row.get('name'),
                    phone=row.get('phone'),
                    city=row.get('city'),
                    localidad=row.get('localidad'),
                    municipio_aledano=row.get('municipio_aledano'),
                    policy_agreed=bool(row.get('policy_agreed', True)),
                    confirmed=bool(row.get('confirmed', True)),
                    suspended=bool(row.get('suspended', False)),
                    roles=[4]  # Rol fijo
                )
                user = create_user(db, user=user_data)

            # Crear ticket
            ticket_data = TicketCreate(
                user_id=user.id,
                event_date_id=int(row['event_date_id']),
                ticket_name=row.get('ticket_name', f"{row.get('name')}"),
                check_in=bool(row.get('check_in', False))
            )
            ticket = create_ticket(db, ticket=ticket_data)
            ticket_db = db.query(Ticket).filter(Ticket.id == ticket.id).first()

            event_datetime = ticket_db.event_date.date_time
            formatted_date = event_datetime.strftime("%d-%m-%Y")  # Formato de fecha
            formatted_time = event_datetime.strftime("%I:%M %p")  # Formato de hora con AM/PM

            # Información del ticket para el correo
            ticket_info = {
                "ticket_name": ticket.ticket_name,
                "event_name": f"{ticket_db.event_date.event.event_name}",
                "event_date": f"{formatted_date}",
                "event_time": f"{formatted_time}",
                "stage_name": ticket_db.event_date.event.stage.stage_name,
                "stage_address": ticket_db.event_date.event.stage.address
            }

            # Enviar correo de confirmación
            asyncio.run(send_confirmation_email(user.email, ticket_info))

            # Crear encuesta
            survey_data = SurveyCreate(
                user_id=user.id,
                age=row.get('age'),
                genere=row.get('genere'),
                education=row.get('education'),
                occupation=row.get('occupation'),
                relationship_theatre=row.get('relationship_theatre'),
                motivations=row.get('motivations'),
                others_motivations=row.get('others_motivations'),
                information_medium=row.get('information_medium'),
                other_events=row.get('other_events'),
                permision_research=bool(row.get('permision_research', True))
            )
            create_survey(db, survey=survey_data)

        print("Datos cargados exitosamente desde el archivo CSV.")

# Ruta del archivo CSV
current_directory = os.path.dirname(os.path.abspath(__file__))  # app/email
static_directory = os.path.abspath(os.path.join(current_directory, "./static"))
file_path = os.path.join(static_directory, "bwitches_database6_converted.csv")
print(file_path)
load_data_from_csv(file_path)

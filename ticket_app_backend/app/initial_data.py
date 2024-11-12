from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.models.role import Role
from app.models.event import Event
from app.models.event_dates import EventDate
from app.models.stage import Stage
from app.models.survey import Survey
from app.models.tickets import Ticket

from app.db.session import SessionLocal, engine

from app.crud.user import create_user
from app.crud.role import create_role
from app.crud.stage import create_stage
from app.crud.event import create_event
from app.crud.event_dates import create_event_date

from app.schemas.user import UserCreate
from app.schemas.role import RoleCreate
from app.schemas.stage import StageCreate
from app.schemas.event import EventCreate
from app.schemas.event_dates import EventDateCreate

def init_db(db: Session) -> None:
    # Crear roles si no existen
    role_admin = db.query(Role).filter(Role.shortname == "admin").first()
    if not role_admin:
        create_role(db, role=RoleCreate(shortname="admin", name_role="administrator", description="This role is for the system administrator."))

    role_theater = db.query(Role).filter(Role.shortname == "theater").first()
    if not role_theater:
        create_role(db, role=RoleCreate(shortname="theater", name_role="theater", description="This role is for the Theater."))

    role_productor = db.query(Role).filter(Role.shortname == "productor").first()
    if not role_productor:
        create_role(db, role=RoleCreate(shortname="productor", name_role="productor", description="This role is for the Productor."))

    role_spectator = db.query(Role).filter(Role.shortname == "spectator").first()
    if not role_spectator:
        create_role(db, role=RoleCreate(shortname="spectator", name_role="spectator", description="This role is for the Spectator."))

    role_logistic = db.query(Role).filter(Role.shortname == "logistic").first()
    if not role_logistic:
        create_role(db, role=RoleCreate(shortname="logistic", name_role="logistic", description="This role is for the Logistic."))

    # Crear un usuario administrador si no existe
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        create_user(db, user=UserCreate(
            email="admin@example.com",
            username="admin",
            password="admin",
            roles=[1, 2, 3, 4, 5],  # Asignar múltiples roles
            name="Admin User",
            confirmed=True,
            policy_agreed=True
        ))

    #Crea un escenario si no existe
    stage = db.query(Stage).first()
    if not stage:
        create_stage(db, stage=StageCreate(
            stage_name="Sala Seki Sano - Corporación Colombiana de Teatro",
            address="Calle 12 # 2-65",
            phone="+57 (1) 3429621",
            capacity=100,
            city="Bogotá",
            departament="Bogotá D.C.",
            user_id=admin_user.id
        ))

    #Crea un evento si no existe
    event = db.query(Event).filter(Event.id == 1).first()
    if not event:
        create_event(db, event=EventCreate(
            event_name="BWitches",
            stage_id=stage.id,
            user_id=admin_user.id,
            pulep="N/A",
            description="Version irresponsable de 'Las Brujas de Salem' de Arthur Miller",
            artistic_team={
                "direccion_general": "Sebastián Illera",
                "adaptacion": "Sebastián Illera - Valentina Méndez",
                "iluminacion": "Quimbaru",
                "coreografia": "Indira Duque",
                "diseno_vestuario": "Alejandra Castro",
                "asistencia_direccion": "Valentina Méndez",
                "elenco": "Lina Boada, Sarita Casas, Gabriela Callejas, Katherine Gregory, Angie Hernandez, Nicoll Leal, Juana Maal, Laura Moreno, Mayelin Niño, Gabriela Otálora, Pablo Pimentel, Valeria Rodríguez, Andrés Restrepo, Esteban Sánchez, Juan Soto y Alejandro Zambrano."
                },
            active=True
        ))

    #Crea event_dates si no existen
    event_dates_exist = db.query(EventDate).filter(EventDate.event_id == event.id).first()
    if not event_dates_exist:
        # Define las fechas y horas de los eventos
        event_dates = [
            {"date_time": datetime(2024, 11, 14, 19, 0), "available_tickets": 100},
            {"date_time": datetime(2024, 11, 15, 19, 0), "available_tickets": 100},
            {"date_time": datetime(2024, 11, 16, 16, 0), "available_tickets": 100},
            {"date_time": datetime(2024, 11, 16, 19, 30), "available_tickets": 100},
            {"date_time": datetime(2024, 11, 17, 18, 0), "available_tickets": 100},
        ]
        # Crea las fechas de evento en la base de datos
        for date in event_dates:
            create_event_date(db, EventDateCreate(
                event_id=event.id,
                date_time=date["date_time"],
                available_tickets=date["available_tickets"]
            ))

        

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

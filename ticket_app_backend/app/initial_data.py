from sqlalchemy.orm import Session

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

from app.schemas.user import UserCreate
from app.schemas.role import RoleCreate
from app.schemas.stage import StageCreate
from app.schemas.event import EventCreate

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
            roles=[role_admin.id, role_theater.id, role_productor.id, role_spectator.id, role_logistic.id],  # Asignar múltiples roles
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
                "Direccion general": "Sebastián Illera",
                "Adaptación": "Sebastián Illera - Valentina Méndez",
                "Iluminación": "Quimbaru",
                "Coreografía": "Indira Duque",
                "Diseño de vestuario": "Alejandra Castro",
                "Asistencia de Dirección": "Valentina Méndez",
                "Elenco": "Lina Boada, Sarita Casas, Gabriela Callejas, Katherine Gregory, Angie Hernandez, Nicoll Leal, Juana Maal, Laura Moreno, Mayelin Niño, Gabriela Otálora, Pablo Pimentel, Valeria Rodríguez, Andrés Restrepo, Esteban Sánchez, Juan Soto y Alejandro Zambrano."
                },
            active=True
        ))

    #Crea event_dates si no existen
    
        

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

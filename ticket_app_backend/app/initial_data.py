from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.db.session import SessionLocal, engine
from app.crud.user import create_user
from app.crud.role import create_role
from app.schemas.user import UserCreate
from app.schemas.role import RoleCreate

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
            role_id=role_admin.id,  # Asignar el ID del rol 'admin'
            name="Admin User",
            confirmed=True,
            policy_agreed=True
        ))

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, List

from app.core.security import hash_password

def create_user(db: Session, user: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos"""
    db_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hash_password(user.password),
        role_id = user.role_id,
        name = user.name,
        phone = user.phone,
        socialmedia = user.socialmedia,
        city = user.city,
        localidad = user.localidad,
        municipio_aledano = user.municipio_aledano,
        first_access = user.first_access,
        picture = user.picture,
        policy_agreed = user.policy_agreed,
        confirmed = user.confirmed,
        suspended = user.suspended,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Obtiene un usuario por ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obtiene un usuario por email"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    """Obtiene una lista de usuarios con paginación"""
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Actualiza un usuario existente"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un usuario por ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True

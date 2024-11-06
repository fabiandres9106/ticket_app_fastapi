from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from typing import Optional, List

def create_role(db: Session, role: RoleCreate) -> Role:
    """Crea un nuevo rol en la base de datos"""
    db_role = Role(
        name_role = role.name_role,
        shortname = role.shortname,
        description = role.description
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_role(db: Session, role_id: int) -> Optional[Role]:
    """Obtiene un rol por ID"""
    return db.query(Role).filter(Role.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 10) -> List[Role]:
    """Obtiene una lista de roles con paginación"""
    return db.query(Role).offset(skip).limit(limit).all()

def update_role(db: Session, role_id: int, role_update: RoleUpdate) -> Optional[Role]:
    """Actualiza un rol que existe"""
    db_role = db.query(Role).filter(Role.id == role_id). first()
    if db_role is None:
        return None
    for key, value in role_update.model_dump(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> bool:
    """Elimina un rol por ID"""
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role is None:
        return False
    db.delete(db_role)
    db.commit()
    return True
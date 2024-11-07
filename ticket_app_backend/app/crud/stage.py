from sqlalchemy.orm import Session
from app.models.stage import Stage
from app.schemas.stage import StageCreate, StageUpdate
from typing import Optional, List

def create_stage(db: Session, stage: StageCreate) -> Stage:
    """Crea un nuevo Stage en BD"""
    db_stage = Stage(
        stage_name = stage.stage_name,
        address = stage.address,
        phone = stage.phone,
        social_media = stage.social_media,
        contact_name = stage.contact_name,
        capacity = stage.capacity,
        city = stage.city,
        departament = stage.departament,
        user_id = stage.user_id
    )
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def get_stage(db: Session, stage_id: int) -> Optional[Stage]:
    """Obtiene un stage por ID"""
    return db.query(Stage).filter(Stage.id == stage_id).first()

def get_stages(db: Session, skip: int = 0, limit: int = 10) -> List[Stage]:
    """Obtiene una lista de stage con paginación"""
    return db.query(Stage).offset(skip).limit(limit).all()

def update_stage(db: Session, stage_id: int, stage_update: StageUpdate) -> Optional[Stage]:
    """Actualiza un stage existente"""
    db_stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if db_stage is None:
        return None
    for key, value in stage_update.model_dump(exclude_unset=True).items():
        setattr(db_stage, key, value)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def delete_stage(db: Session, stage_id: int) -> bool:
    """Elimina un stage por ID"""
    db_stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if db_stage is None:
        return False
    db.delete(db_stage)
    db.commit()
    return True
from sqlalchemy.orm import Session
from app.models.survey import Survey
from app.schemas.survey import SurveyCreate, SurveyUpdate
from typing import Optional, List

def create_survey(db: Session, survey: SurveyCreate) -> Survey:
    """Crea un nuevo Survey en BD"""
    db_survey = Survey(
        user_id = survey.user_id,
        age = survey.age,
        genere = survey.genere,
        education = survey.education,
        occupation = survey.occupation,
        relationship_theatre = survey.relationship_theatre,
        motivations = survey.motivations,
        others_motivations = survey.others_motivations,
        information_medium = survey.information_medium,
        other_events = survey.other_events,
        permision_research = survey.permision_research,
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def get_survey(db: Session, survey_id: int) -> Optional[Survey]:
    """Obtiene un Survey por ID"""
    return db.query(Survey).filter(Survey.id == survey_id).first()

def get_surveys(db: Session, skip: int = 0, limit: int = 10) -> List[Survey]:
    """Obtiene una lista de Survey con paginación"""
    return db.query(Survey).offset(skip).limit(limit).all()

def update_survey(db: Session, survey_id: int, survey_update: SurveyUpdate) -> Optional[Survey]:
    """Actualiza un Survey existente"""
    db_survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if db_survey is None:
        return None
    for key, value in survey_update.model_dump(exclude_unset=True).items():
        setattr(db_survey, key, value)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def delete_survey(db: Session, survey_id: int) -> bool:
    """Elimina un Survey por ID"""
    db_survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if db_survey is None:
        return False
    db.delete(db_survey)
    db.commit()
    return True
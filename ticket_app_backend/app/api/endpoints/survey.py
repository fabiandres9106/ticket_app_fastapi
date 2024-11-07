from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.survey import create_survey, get_survey, get_surveys, update_survey, delete_survey
from app.schemas.survey import SurveyCreate, SurveyRead, SurveyUpdate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=SurveyRead)
def create_survey_endpoint(survey: SurveyCreate, db: Session = Depends(get_db)):
    db_survey = create_survey(db=db, survey=survey)
    return db_survey

@router.get("/{survey_id}", response_model=SurveyRead)
def read_survey(survey_id: int, db: Session = Depends(get_db)):
    db_survey = get_survey(db=db, survey_id=survey_id)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@router.get("/", response_model=List[SurveyRead])
def read_surveys(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_surveys(db=db, skip=skip, limit=limit)

@router.put("/{survey_id}", response_model=SurveyRead)
def update_survey_endpoint(survey_id: int, survey: SurveyUpdate, db: Session = Depends(get_db)):
    db_survey = update_survey(db=db, survey_id=survey_id, survey_update=survey)
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@router.delete("/{survey_id}", response_model=bool)
def delete_survey_endpoint(survey_id: int, db: Session = Depends(get_db)):
    success = delete_survey(db=db, survey_id=survey_id)
    if not success:
        raise HTTPException(status_code=404, detail="Survey not found")
    return success
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.stage import create_stage, get_stage, get_stages, update_stage, delete_stage
from app.schemas.stage import StageCreate, StageRead, StageUpdate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=StageRead)
def create_stage_endpoint(stage: StageCreate, db: Session = Depends(get_db)):
    db_stage = create_stage(db=db, stage=stage)
    return db_stage

@router.get("/{stage_id}", response_model=StageRead)
def read_stage(stage_id: int, db: Session = Depends(get_db)):
    db_stage = get_stage(db=db, stage_id=stage_id)
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    return db_stage

@router.get("/", response_model=List[StageRead])
def read_stages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_stages(db=db, skip=skip, limit=limit)

@router.put("/{stage_id}", response_model=StageRead)
def update_stage_endpoint(stage_id: int, stage: StageUpdate, db: Session = Depends(get_db)):
    db_stage = update_stage(db=db, stage_id=stage_id, stage_update=stage)
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    return db_stage

@router.delete("/{stage_id}", response_model=bool)
def delete_stage_endpoint(stage_id: int, db: Session = Depends(get_db)):
    success = delete_stage(db=db, stage_id=stage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Stage not found")
    return success
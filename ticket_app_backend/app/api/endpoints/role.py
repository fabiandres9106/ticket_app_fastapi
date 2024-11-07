from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.role import create_role, get_role, get_roles, update_role, delete_role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.db.session import get_db

router = APIRouter()

@router.post("/",response_model=RoleRead)
def create_role_endpoint(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = create_role(db=db, role=role)
    return db_role

@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/", response_model=List[RoleRead])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_roles(db=db, skip=skip, limit=limit)

@router.put("/{role_id}", response_model=RoleRead)
def update_role_endpoint(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = update_role(db=db, role_id=role_id, role_update=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.delete("/{role_id}", response_model=bool)
def delete_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    success = delete_role(db=db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return success

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session, subqueryload
from sqlalchemy import asc, desc
from typing import List

from app.models.user import User
from app.crud.user import create_user, get_user, get_users, update_user, delete_user, check_email_exists
from app.schemas.user import UserCreate, UserRead, UserUpdate, EmailExistsResponse
from app.schemas.role import RoleRead
from app.schemas.survey import SurveyRead

from app.db.session import get_db

from app.core.dependencies import get_current_user

import json


router = APIRouter()

@router.post("/create", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id == "me":
        return current_user
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("", response_model=List[UserRead])
@router.get("/", response_model=List[UserRead])
def read_users(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Leer parámetros de consulta
    range_param = request.query_params.get("range", "[0,9]")
    sort_param = request.query_params.get("sort", '["id", "ASC"]')
    filter_param = request.query_params.get("filter", "{}")

    try:
        range_ = json.loads(range_param)
        sort = json.loads(sort_param)
        filters = json.loads(filter_param)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing query parameters: {str(e)}")

    start, end = range_
    sort_field, sort_order = sort

    # Construir la query base
    query = db.query(User)

    # Aplicar filtros simples (ej: ?filter={"name":"Ana"})
    for attr, value in filters.items():
        if hasattr(User, attr):
            query = query.filter(getattr(User, attr).ilike(f"%{value}%"))

    total = query.count()

    # Ordenar
    sort_column = getattr(User, sort_field, None)
    if sort_column is not None:
        if sort_order == "ASC":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

    # Paginación
    users = query.offset(start).limit(end - start + 1).all()

    # Construir lista
    users_with_roles = [
        UserRead(
            id=user.id,
            email=user.email,
            roles=[RoleRead(id=role.id, name_role=role.name_role, shortname=role.shortname, description=role.description) for role in user.roles],
            username=user.username,
            name=user.name,
            phone=user.phone,
            socialmedia=user.socialmedia,
            city=user.city,
            localidad=user.localidad,
            municipio_aledano=user.municipio_aledano,
            first_access=user.first_access,
            last_access=user.last_access,
            picture=user.picture,
            policy_agreed=user.policy_agreed,
            confirmed=user.confirmed,
            suspended=user.suspended,
            created_at=user.created_at,
            tickets=user.tickets
        )
        for user in users
    ]

    # Cabecera Content-Range con "items" como espera React Admin
    response.headers["Content-Range"] = f"items {start}-{start + len(users) - 1}/{total}"
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"

    return users_with_roles


@router.get("/email_exists/{email}", response_model=EmailExistsResponse)
def email_exists(email: str, db: Session = Depends(get_db)):
    user = check_email_exists(db, email)
    if user:
        return {"exists": True, "user_id": user.id}
    return {"exists": False}

@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=bool)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

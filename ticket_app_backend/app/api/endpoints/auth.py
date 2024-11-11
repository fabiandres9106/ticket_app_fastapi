from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin, UserRead
from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_email
from app.db.session import get_db
from app.schemas.auth import Token 
from app.schemas.role import RoleSchema

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Utiliza model_validate para cada rol en db_user.roles
    roles = [RoleSchema.model_validate(role) for role in db_user.roles]
    
    access_token = create_access_token(data={
        "user_id": db_user.id,
        "email": db_user.email,
        "roles": [role.shortname for role in roles]  # O envía la lista completa de roles si lo prefieres
    })
    return {"access_token": access_token, "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin, UserRead
from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_email
from app.db.session import get_db
from app.schemas.auth import Token 

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Crea una lista con solo los shortname de los roles del usuario
    roles = [role.shortname for role in db_user.roles]
    
    # Crea el token de acceso incluyendo los datos del usuario y los roles
    access_token = create_access_token(data={
        "user_id": db_user.id,
        "email": db_user.email,
        "roles": roles  # Incluye los roles como un JSON en el token
    })
    
    return {"access_token": access_token, "token_type": "bearer"}
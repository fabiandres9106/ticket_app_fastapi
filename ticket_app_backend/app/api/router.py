from fastapi import APIRouter
from app.api.endpoints import user
from app.api.endpoints import role

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(role.router, prefix="/roles", tags=["roles"])
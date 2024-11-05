from sqlalchemy import func, Column, Integer, String, JSON, DateTime, Boolean
from datetime import datetime
from app.db.base import Base
from pydantic import BaseModel, EmailStr

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(Integer(), nullable=False)
    name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    socialmedia = Column(JSON, nullable=True)
    city = Column(String(255), nullable=True)
    localidad = Column(String(255), nullable=True)
    municipio_aledano = Column(String(255), nullable=True)
    first_access = Column(DateTime, nullable=True)
    last_access = Column(DateTime, onupdate=func.now())
    picture = Column(String(255), nullable=True)
    policy_agreed = Column(Boolean, default=True)
    confirmed = Column(Boolean, default=True)
    suspended = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class UserCreate(BaseModel):
    username: str
    email: EmailStr

from sqlalchemy import func, ForeignKey, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime
from app.db.base import Base
from pydantic import BaseModel, EmailStr

from app.models.user import User

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    stage_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    social_media = Column(JSON, nullable=True)
    contact_name = Column(String(255), nullable=True)
    capacity = Column(Integer(), nullable=False)
    city = Column(String(50), nullable=True)
    departament = Column(String(50), nullable=True)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship('User')
from sqlalchemy import func, Column, Integer, String, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base
from pydantic import BaseModel

from app.models.user import User

class Survey(Base):
    __tablename__ = "survey"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    age = Column(String(20), nullable=True)
    genere = Column(String(50), nullable=True)
    education = Column(String(50), nullable=True)
    occupation = Column(String(100), nullable=True)
    relationship_theatre = Column(String(50), nullable=True)
    motivations = Column(JSON, nullable=True)
    others_motivations = Column(String(255), nullable=True)
    information_medium = Column(String(50), nullable=True)
    other_events = Column(JSON, nullable=True)
    permision_research = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship('User', back_populates="surveys")

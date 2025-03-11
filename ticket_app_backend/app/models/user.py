from sqlalchemy import func, ForeignKey, Column, Integer, String, JSON, DateTime, Boolean, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

from app.models.role import Role

from datetime import datetime

# Tabla de asociación entre usuarios y roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
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

    # Relación muchos a muchos con Role
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    # Relación con el modelo Ticket
    tickets = relationship("Ticket", back_populates="user")
    # Relación con el modelo Survey
    surveys = relationship("Survey", back_populates="user")

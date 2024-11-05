from sqlalchemy import func, Column, Integer, String

from app.db.base import Base

from pydantic import BaseModel

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name_role = Column(String(50), nullable=True)
    shortname = Column(String(20), nullable=False)
    description = Column(String(255), nullable=True)

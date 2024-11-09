from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, List
from datetime import datetime

class RoleRead(BaseModel):
    id: int
    name: str
    shortname: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    roles: List[int] 
    username: Optional[str] = None
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    socialmedia: Optional[Any] = None
    city: Optional[str] = None
    localidad: Optional[str] = None
    municipio_aledano: Optional[str] = None
    first_access: Optional[datetime] = None
    picture: Optional[str] = None
    policy_agreed: bool = True
    confirmed: bool = True
    suspended: bool = False

class UserRead(BaseModel):
    id: int
    email: EmailStr
    roles: List[RoleRead]
    username: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    socialmedia: Optional[Any]
    city: Optional[str]
    localidad: Optional[str]
    municipio_aledano: Optional[str]
    first_access: Optional[datetime]
    last_access: Optional[datetime]
    picture: Optional[str]
    policy_agreed: bool
    confirmed: bool
    suspended: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    roles: List[int] 
    name: Optional[str]
    phone: Optional[str]
    socialmedia: Optional[Any]
    city: Optional[str]
    localidad: Optional[str]
    municipio_aledano: Optional[str]
    first_access: Optional[str]
    picture: Optional[str]
    policy_agreed: Optional[str]
    confirmed: Optional[str]
    suspended: Optional[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str
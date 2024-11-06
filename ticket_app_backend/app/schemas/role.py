from pydantic import BaseModel
from typing import Optional, Any

class RoleCreate(BaseModel):
    name_role: Optional[str] = None
    shortname: str
    description: Optional[str] = None

class RoleRead(BaseModel):
    id: int
    name_role: Optional[str]
    shortname: str
    description: Optional[str]

    class Config:
        orm_mode = True

class RoleUpdate(BaseModel):
    name_role: Optional[str]
    shortname: str
    description: Optional[str]

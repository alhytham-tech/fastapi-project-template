from typing import List, Optional
from pydantic import BaseModel

from mixins.schemas import BaseUACSchemaMixin



class PermissionCreate(BaseModel):
    name: str
    description: Optional[str]


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionSchema(BaseUACSchemaMixin):
    
    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    name: str
    description: Optional[str]


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleSchema(BaseUACSchemaMixin):
    permissions: List[PermissionSchema]
    
    class Config:
        orm_mode = True
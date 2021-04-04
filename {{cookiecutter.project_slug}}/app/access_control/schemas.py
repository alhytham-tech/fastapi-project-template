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
    permissions: Optional[List[str]]


class RemoveRolePermission(BaseModel):
    permissions: List[str]


class RoleSchema(BaseUACSchemaMixin):
    permissions: List[PermissionSchema]
    
    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    name: str
    description: Optional[str]


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    roles: Optional[List[str]]


class RemoveGroupRole(BaseModel):
    roles: List[str]


class GroupSchema(BaseUACSchemaMixin):
    roles: List[RoleSchema]
    
    class Config:
        orm_mode = True
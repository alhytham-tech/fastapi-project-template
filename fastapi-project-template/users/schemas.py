from typing import List, Optional
from pydantic import BaseModel, EmailStr

from mixins.schemas import BaseSchemaMixin
from access_control.schemas import GroupSchema



class UserCreate(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    middlename: Optional[str]
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    middlename: Optional[str] = None
    password: Optional[str] = None


class UserSchema(BaseSchemaMixin):
    email: EmailStr
    firstname: str
    lastname: str
    middlename: str
    is_active: bool
    is_superuser: bool
    group: GroupSchema = None

    @property
    def permissions(self) -> List[str]:
        perms = []
        for role in self.group.roles:
            for perm in role.permissions:
                perms.append(perm.name)
        return perms

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    class Config:
        orm_mode = True

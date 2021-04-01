from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from config.db import Base
from mixins.columns import BaseMixin, BaseUACMixin



# Many to Many associations
permission_role = Table('permission_role', Base.metadata,
    Column('permission_id', Integer, ForeignKey('permissions.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


class Permission(BaseUACMixin, Base):
    pass


class Role(BaseUACMixin, Base):
    permissions = relationship("Permission", secondary=permission_role)
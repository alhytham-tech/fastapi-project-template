from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from config.db import Base
from mixins.columns import BaseMixin



user_group = Table('user_group', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class User(BaseMixin, Base):
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    old_password_hash = Column(ARRAY(String(255)))
    firstname = Column(String(255))
    lastname = Column(String(255))
    middlename = Column(String(255))
    phone = Column(String(50))
    is_active =  Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    groups = relationship("Group", secondary=user_group)

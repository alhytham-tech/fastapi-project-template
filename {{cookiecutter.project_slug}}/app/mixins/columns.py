from datetime import datetime, timezone
import uuid

import inflect

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr



get_plural = inflect.engine()


class BaseMixin:
    '''
    Provides id, created_at and last_modified columns
    '''
    @declared_attr
    def __tablename__(cls):
        try:
            table_name = cls.__tablename__
        except RecursionError:
            pass
        plural_name = get_plural.plural_noun(cls.__name__.lower())
        return plural_name

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_modified = Column( DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )


class BaseUACMixin(BaseMixin):
    '''
    Defines common columns for user access control models
    '''
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
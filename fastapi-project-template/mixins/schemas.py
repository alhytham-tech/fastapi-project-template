from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4



class BaseSchemaMixin(BaseModel):
    id: int
    uuid: UUID4
    created_at: datetime
    last_modified: datetime


class BaseUACSchemaMixin(BaseSchemaMixin):
    name: str
    description: Optional[str]
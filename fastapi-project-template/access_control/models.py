from config.db import Base
from mixins.columns import BaseMixin, BaseUACMixin



class Permission(BaseUACMixin, Base):
    pass

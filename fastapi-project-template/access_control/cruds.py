from sqlalchemy.orm import Session

from access_control import models, schemas



def create_permission(db: Session, perm_data: schemas.PermissionCreate):
    permission = models.Permission(**perm_data.dict(exclude_unset=True))
    permission.name = permission.name.lower()
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission
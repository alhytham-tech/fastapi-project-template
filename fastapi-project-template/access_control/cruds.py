from sqlalchemy.orm import Session

from access_control import models, schemas



def create_permission(db: Session, perm_data: schemas.PermissionCreate):
    permission = models.Permission(**perm_data.dict(exclude_unset=True))
    permission.name = permission.name.lower()
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def get_perm_by_name(db: Session, name: str):
    return db.query(models.Permission). \
        filter(models.Permission.name == name). \
        one()


def create_role(db: Session, role_data: schemas.RoleCreate):
    role = models.Role(**role_data.dict(exclude_unset=True))
    role.name = role.name.lower()
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

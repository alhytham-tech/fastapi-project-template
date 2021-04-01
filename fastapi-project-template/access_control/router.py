from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import dependencies as deps
from access_control import cruds, models, schemas



perms_router = APIRouter(
    prefix='/permissions',
    tags=['Permissions']
)
roles_router = APIRouter(
    prefix='/roles',
    tags=['Roles']
)


# Permissions
@perms_router.post('',
    status_code=201,
    response_model=schemas.PermissionSchema
)
def create_permission(
    perm_data: schemas.PermissionCreate,
    dba: Session = Depends(deps.get_db)
):
    try:
        permission = cruds.create_permission(db=dba, perm_data=perm_data)
    except IntegrityError as e:
        raise HTTPException(
            status_code=403,
            detail='Duplicate permission not allowed'
        )
    else:
        return permission


@perms_router.get('', response_model=List[schemas.PermissionSchema])
def list_permissions(dba: Session = Depends(deps.get_db)):
    return dba.query(models.Permission).all()


@perms_router.get('/{perm_name}',response_model=schemas.PermissionSchema)
def permission_detail(perm_name: str, dba: Session = Depends(deps.get_db)):
    try:
        permission = cruds.get_perm_by_name(name=perm_name, db=dba)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Permission not found'
        )
    else:
        return permission


@perms_router.put('/{perm_name}', response_model=schemas.PermissionSchema)
def update_permission(
    perm_name: str,
    perm_data: schemas.PermissionUpdate,
    dba: Session = Depends(deps.get_db)
):
    try:
        permission = cruds.get_perm_by_name(name=perm_name, db=dba)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Permission not found'
        )
    else:
        perm_update_dict = perm_data.dict(exclude_unset=True)
        if len(perm_update_dict) < 1:
            raise HTTPException(
                status_code=400,
                detail='Invalid request'
            )
        for key, value in perm_update_dict.items():
            setattr(permission, key, value)
        dba.commit()
        dba.refresh(permission)
        return permission


@perms_router.delete('/{perm_name}')
def delete_permission(perm_name: str, dba: Session = Depends(deps.get_db)):
    try:
        tag = cruds.get_perm_by_name(db=dba, name=perm_name)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Permission not found'
        )
    else:
        dba.query(models.Permission). \
            filter(models.Permission.name == perm_name). \
            delete()
        dba.commit()
        return {'detail': 'Permission deleted successfully.'}

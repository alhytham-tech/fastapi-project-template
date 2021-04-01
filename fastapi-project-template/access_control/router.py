from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import dependencies as deps
from access_control import cruds, models, schemas




perms_router = APIRouter(
    prefix='/permissions',
    tags=['Permissions']
)


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
            status_code=400,
            detail='This permission name is already in use'
        )
    else:
        return permission


@perms_router.get('', response_model=List[schemas.PermissionSchema])
def list_permissions(dba: Session = Depends(deps.get_db)):
    return dba.query(models.Permission).all()

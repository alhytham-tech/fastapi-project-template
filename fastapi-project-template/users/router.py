from typing import List
from pydantic import UUID4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import dependencies as deps
from users import cruds, models, schemas
from access_control.cruds import get_group_by_name
from utils.users import get_password_hash, verify_password



users_router = APIRouter(
    prefix='/users',
    tags=['User']
)

auth_router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@users_router.post('',
    status_code=201,
    response_model=schemas.UserSchema
)
def create_user(
    user_data: schemas.UserCreate,
    dba: Session = Depends(deps.get_db)
):
    try:
        user = cruds.create_user(db=dba, user_data=user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=403,
            detail='This email is already in use'
        )
    return user


@users_router.get('', response_model=List[schemas.UserSchema])
def list_users(dba: Session = Depends(deps.get_db)):
    return dba.query(models.User).all()


@users_router.get('/{uuid}', response_model=schemas.UserSchema)
def user_detail(uuid: UUID4, dba: Session = Depends(deps.get_db)):
    user = cruds.get_user_by_uuid(uuid=uuid, db=dba)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user


@users_router.put('/{uuid}', response_model=schemas.UserSchema)
def update_user(
    uuid: UUID4,
    user_data: schemas.UserUpdate,
    dba: Session = Depends(deps.get_db)
):
    user = cruds.get_user_by_uuid(uuid=uuid, db=dba)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    user_update_dict = user_data.dict(exclude_unset=True)
    if len(user_update_dict) < 1:
        raise HTTPException(
            status_code=400,
            detail='Invalid request'
        )

    for key, value in user_update_dict.items():
        setattr(user, key, value)
    dba.commit()
    dba.refresh(user)
    return user


@users_router.delete('/{uuid}')
def delete_user(uuid: UUID4, dba: Session = Depends(deps.get_db)):
    user = cruds.get_user_by_uuid(db=dba, uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    dba.query(models.User). \
        filter(models.User.uuid == uuid). \
        delete()
    dba.commit()
    return {'detail': 'User deleted successfully.'}


@users_router.post(
    '/{uuid}/groups',
    response_model=schemas.UserSchema
)
def add_group_to_user(
    uuid: UUID4, groups: schemas.UserGroup, dba: Session = Depends(deps.get_db)
):
    user = cruds.get_user_by_uuid(db=dba, uuid=uuid)
    group_list = groups.dict().pop('groups')
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    for group_name in group_list:
        group = get_group_by_name(name=group_name, db=dba)
        if not group:
            raise HTTPException(
                status_code=404,
                detail=f'{group_name} is not found'
            )
        user.groups.append(group)
    dba.commit()
    dba.refresh(user)
    return user


@users_router.delete(
    '/{uuid}/groups',
    response_model=schemas.UserSchema
)
def remove_group_from_user(
    uuid: UUID4, groups: schemas.UserGroup, dba: Session = Depends(deps.get_db)
):
    user = cruds.get_user_by_uuid(db=dba, uuid=uuid)
    group_list = groups.dict().pop('groups')
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    for group_name in group_list:
        group = get_group_by_name(name=group_name, db=dba)
        if not group:
            raise HTTPException(
                status_code=404,
                detail=f'{group_name} is not found'
            )
        user.groups.remove(group)
    dba.commit()
    dba.refresh(user)
    return user


@users_router.post('/{uuid}/password')
def change_user_password(
    uuid: UUID4,
    passwords: schemas.ChagePasswordFromDashboard,
    dba: Session = Depends(deps.get_db)
):
    user = cruds.get_user_by_uuid(db=dba, uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    if not verify_password(passwords.current_password, user.password_hash):
        raise HTTPException(
            status_code=403,
            detail='Current password is incorrect'
        )
    new_password_hash = get_password_hash(passwords.new_password)
    user.password_hash = new_password_hash
    dba.commit()
    dba.refresh(user)
    return {'detail': 'Password changed successfully.'}
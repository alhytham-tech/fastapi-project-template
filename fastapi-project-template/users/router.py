from typing import List
from pydantic import UUID4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import dependencies as deps
from users import cruds, models, schemas



users_router = APIRouter(
    prefix='/users',
    tags=['User']
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


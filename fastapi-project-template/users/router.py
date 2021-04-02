from typing import List
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


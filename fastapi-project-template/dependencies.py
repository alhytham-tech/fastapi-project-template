from jose import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from decouple import config as decouple_config
from fastapi.security import OAuth2PasswordBearer

from config import db



SECRET_KEY = decouple_config('SECRET_KEY')
TOKEN_URL = decouple_config('DOCS_AUTH_URL', default='token')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_db():
    dbase = db.SessionLocal()
    try:
        yield dbase
    finally:
        dbase.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = users_schema.UserSchema.from_orm(
        users_cruds.get_user_by_email(db=db, email=payload['email'])
    )
    return user

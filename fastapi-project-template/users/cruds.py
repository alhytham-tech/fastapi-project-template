from pydantic import EmailStr, UUID4
from sqlalchemy.orm import Session

from users import models, schemas
from utils.users import get_password_hash, verify_password


def create_user(db: Session, user_data: schemas.UserCreate):
    user_dict = user_data.dict()
    unhashed_password = user_dict.pop('password')
    hashed_password = get_password_hash(unhashed_password)
    user_dict['password_hash'] = hashed_password
    user = models.User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_uuid(db: Session, uuid: UUID4):
    return db.query(models.User).filter(models.User.uuid == uuid).first()


def authenticate_user(email: EmailStr, password: str, dba: Session):
    user = get_user_by_email(db=dba, email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='Email and password do not match'
        )
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail='Email and password do not match'
        )
    return schema.UserSchema.from_orm(user) 

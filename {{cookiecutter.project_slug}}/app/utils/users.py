from datetime import datetime, timedelta

from decouple import config as decouple_config
from jose import JWTError, jwt
from passlib.context import CryptContext



# Password hash context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# JWT config
SECRET_KEY = decouple_config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = decouple_config('AUTH_TOKEN_EXPIRES', cast=int)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

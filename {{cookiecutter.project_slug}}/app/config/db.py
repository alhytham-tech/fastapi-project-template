from decouple import config as decouple_config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# Database server config
DB_HOST = decouple_config('DB_HOST')
DB_PORT = decouple_config('DB_PORT', cast=int)
DB_USER = decouple_config('DB_USER')
DB_NAME = decouple_config('DB_NAME')
DB_ENGINE = decouple_config('DB_ENGINE', default='postgres')
DB_PASSWORD = decouple_config('DB_PASSWORD')

DB_URL = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# SQLAlchemy config

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
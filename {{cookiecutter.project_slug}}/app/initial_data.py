import logging
from sqlalchemy.exc import ProgrammingError

from config.init_db import init_db
from config.db import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FastAPI Template')
user = {
    'email': '{{cookiecutter.superuser_email}}',
    'password': '{{cookiecutter.superuser_password}}'
}
date_created = '''\n
Use the info below to login:
email: {{cookiecutter.superuser_email}}
password: {{cookiecutter.superuser_password}}\n
'''

def init() -> None:
    db = SessionLocal()
    init_db(db, **user)


def main() -> None:
    try:
        logger.info('Creating initial data')
        init()
        logger.info('Initial data created')
        logger.info(date_created)
    except ProgrammingError:
        logger.error(
            ' Cannot find tables on your database. '
            'Have you ran migrations with "alembic upgrade head"?'
        )

if __name__ == "__main__":
    main()
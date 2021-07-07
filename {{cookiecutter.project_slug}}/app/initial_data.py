import os
import logging
from sys import argv
from sqlalchemy.exc import ProgrammingError

from config.init_db import init_db
from config.db import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(' [FastAPI Template]')

def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    try:
        logger.info(' Creating initial data...')
        init()
        logger.info(' Initial data created.')
    except ProgrammingError:
        logger.error(
            ' Cannot find tables on your database. '
            'Have you ran migrations with "alembic upgrade head"?'
        )

if __name__ == '__main__':
    main()
    # Auto delete this file 'app/initial_data.py' &
    #'app/config/init_db.py' after use.
    os.remove(os.path.join(os.getcwd(), 'config', 'init_db.py'))
    os.remove(argv[0])
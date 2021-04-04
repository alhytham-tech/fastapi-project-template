import logging

from config.init_db import init_db
from config.db import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FastAPI Template')
date_created = '''\n
Use the info below to login:
email: admin@example.com
password: superadminpassword\n
'''

def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info('Creating initial data')
    init()
    logger.info('Initial data created')
    logger.info(date_created)


if __name__ == "__main__":
    main()
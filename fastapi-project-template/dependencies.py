from config import db



def get_db():
    dbase = db.SessionLocal()
    try:
        yield dbase
    finally:
        dbase.close()
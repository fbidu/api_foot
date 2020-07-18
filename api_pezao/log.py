from .database import SessionLocal
from .models.log import Log


def log(message, db=None, **kwargs):
    """
    Creates a new log
    """
    db_log = Log(message=message, **kwargs)

    if not db:
        db = SessionLocal()

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

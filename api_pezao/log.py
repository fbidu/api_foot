"""
Módulo que oferece funções para log
"""
import logging
from .database import SessionLocal
from .models.log import Log


def log(message, db=None, level=logging.INFO, **kwargs):
    """
    Creates a new log
    """
    logging.log(level, message)
    db_log = Log(message=message, **kwargs)

    if not db:
        db = SessionLocal()

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

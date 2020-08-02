"""
Módulo que oferece funções para log
"""
import logging
import os

from .database import SessionLocal
from .models.log import Log


def log(message, db=None, level=logging.INFO, override_test=False, **kwargs):
    """
    Creates a new log
    """
    logging.log(level, message)

    if not override_test and "PYTEST_CURRENT_TEST" in os.environ:
        return

    db_log = Log(message=message, **kwargs)

    if not db:
        db = SessionLocal()

    db.add(db_log)
    db.commit()
    db.flush()

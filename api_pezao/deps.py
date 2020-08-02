"""
Common dependencies
"""
from functools import lru_cache

from . import config
from .database import SessionLocal


def get_db():
    """
    Returns a new DB instance
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # pylint: disable=no-member


@lru_cache()
def get_settings():
    """
    Returns a new instance of settings
    """
    return config.Settings()

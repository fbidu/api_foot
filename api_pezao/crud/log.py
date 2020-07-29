"""
CRUD for logs
"""
from typing import List

from sqlalchemy.orm import Session

from ..models import Log


def list_logs(db: Session) -> List[Log]:
    """
    Lists all the registered users
    """
    return db.query(Log).all()

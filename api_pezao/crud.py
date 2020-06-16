"""
CRUD = Create Read Update Delete
"""

from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user from the data in the schema inside the provided DB
    """
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def list_users(db: Session):
    """
    Lists all the registered users
    """
    return db.query(models.User).all()

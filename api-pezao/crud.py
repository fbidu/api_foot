"""
CRUD = Create Read Update Delete
"""

from sqlalchemy.orm import Session

from . import models, schema


def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def list_users(db: Session):
    return db.query(models.User).all()

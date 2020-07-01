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


def find_user(db: Session, email: str = None, cpf: str = None):
    """
    Procura por um usuário por email ou cpf.
    Se tanto e-mail quanto cpf forem fornecidos,
    os dois devem existir no cadastro do usuário.
    """
    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)

    if cpf:
        query = query.filter(models.User.cpf == cpf)

    return query.first()

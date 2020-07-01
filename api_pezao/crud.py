"""
CRUD = Create Read Update Delete
"""
from typing import List

from sqlalchemy.orm import Session

from api_pezao.models.user import User


from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> User:
    """
    Creates a new user from the data in the schema inside the provided DB
    """
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def list_users(db: Session) -> List[User]:
    """
    Lists all the registered users
    """
    return db.query(models.User).all()


def find_user(db: Session, email: str = None, cpf: str = None) -> User:
    """
    Procura por um usuário por email ou cpf.

    Se os dois campos - email e cpf - forem fornecidos,
    essa função vai buscar por usuário que tenha tanto o
    e-mail quanto o CPF igual ao da função.

    Args:
        db (sqlalchemy.orm.Session): Sessão do SQLAlchemy para buscar o usuário
        email (str, opcional): e-mail para ser buscado
        cpf (str, opcional): CPF para ser buscado
    """
    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)

    if cpf:
        query = query.filter(models.User.cpf == cpf)

    return query.first()

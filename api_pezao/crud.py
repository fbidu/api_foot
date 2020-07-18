"""
CRUD = Create Read Update Delete
"""

from typing import List

from sqlalchemy.orm import Session

from api_pezao.models.log import Log
from api_pezao.models.user import User


from . import models, schemas
from .auth import get_password_hash


def create_user(db: Session, user: schemas.UserCreate) -> User:
    """
    Creates a new user from the data in the schema inside the provided DB
    """
    db_user = models.User(**user.dict())
    db_user.password = get_password_hash(db_user.password)

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

    Se nenhum dos campos for fornecido, a função retorna None

    Args:
        db (sqlalchemy.orm.Session): Sessão do SQLAlchemy para buscar o usuário
        email (str, opcional): e-mail para ser buscado
        cpf (str, opcional): CPF para ser buscado
    """

    if not (email or cpf):
        return None

    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)
    if cpf:
        query = query.filter(models.User.cpf == cpf)

    return query.first()


def get_current_user(db: Session, token: str):
    """
    Retorna informações do usuário logado
    """
    user = find_user(db, email=token)
    return user


def list_logs(db: Session) -> List[Log]:
    """
    Lists all the registered users
    """
    return db.query(models.Log).all()

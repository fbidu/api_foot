"""
CRUD = Create Read Update Delete
"""

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import get_password_hash
from ..models import User


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


def set_staff_role(user: schemas.User, staff: bool, db: Session) -> User:
    """
    Muda um usuário para staff
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_staff = staff
        db.commit()
        db.refresh(db_user)

    return db_user


def set_superuser_role(user: schemas.User, superuser: bool, db: Session) -> User:
    """
    Muda um usuário para super_user
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_superuser = superuser
        db.commit()
        db.refresh(db_user)

    return db_user


def list_users(db: Session) -> List[User]:
    """
    Lists all the registered users
    """
    return db.query(models.User).all()


def find_user(db: Session, username: str) -> User:
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

    query = db.query(models.User)
    user = query.filter(models.User.cpf == username).first()

    if user is None:
        user = query.filter(models.User.email == username).first()
    if user is None:
        user = query.filter(models.User.login == username).first()

    return user


def get_current_user(db: Session, token: str):
    """
    Retorna informações do usuário logado
    """
    user = find_user(db, username=token)
    return user

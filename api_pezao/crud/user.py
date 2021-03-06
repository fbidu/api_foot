"""
CRUD = Create Read Update Delete
"""
import re
from random import choices
from string import ascii_letters, digits
from typing import List, Tuple

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import log, models, schemas
from ..auth import SECRET_KEY, get_password_hash
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
    return db.query(models.User).filter(~models.User.deleted).all()


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

    query = db.query(models.User).filter(~models.User.deleted)

    cpf_username = "".join(re.findall(r"\d", username))

    user = query.filter(models.User.cpf == cpf_username).first()

    if user is None:
        user = query.filter(models.User.email == username).first()
    if user is None:
        user = query.filter(models.User.login == username).first()

    return user


def get_current_user(db: Session, token: str):
    """
    Retorna informações do usuário logado
    """
    try:
        token = jwt.decode(token, SECRET_KEY)
        user = find_user(db, username=token["sub"])
    except JWTError:
        return None

    return user


def delete_user(db: Session, user_id: int) -> schemas.User:
    """
    Deleta um usuário usando de soft_delete
    """
    db_user = db.query(User).get(user_id)
    db_user.deleted = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_patient_user(db: Session, cpf: str, name: str) -> Tuple[User, str]:
    """
    Cria um usuário para paciente com base em seu `cpf`.

    Retorna o objeto criado no banco e uma senha aleatória criada
    para o usuário.
    """
    db_user = find_user(db, username=cpf)

    # Usuário já existe
    if db_user:
        return db_user, None

    password = "".join(choices(ascii_letters + digits, k=8))
    user = schemas.UserCreate(cpf=cpf, name=name, password=password)
    db_user = create_user(db, user)

    log(f"Criado usuário para paciente com cpf {cpf} e senha {password}")

    return (db_user, password)

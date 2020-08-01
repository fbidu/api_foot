"""
Testes unitários para as funções de banco de dados
"""
from pytest import fixture
from sqlalchemy.orm import Session

from api_pezao import auth, crud
from api_pezao.models import User

from .db_utils import create_test_user

# pylint: disable=redefined-outer-name


@fixture
def test_user(db) -> User:
    """
    Cria um usuário de teste para ser usado nas funções abaixo
    """
    return create_test_user(db)


def test_find_user_by_email(db: Session, test_user: User):
    """
    Testa se conseguimos encontrar um usuário por email
    """
    found_user = crud.find_user(db, username="test@test.com")

    assert found_user
    assert test_user == found_user


def test_find_user_by_cpf(db: Session, test_user: User):
    """
    Testa se conseguimos encontrar um usuário por cpf
    """
    found_user = crud.find_user(db, username="00000000000")

    assert found_user
    assert test_user == found_user


def test_create_patient_user(db: Session):
    """
    Testa a criação de um usuário para um paciente
    """

    cpf = "00000000000"
    user, password = crud.create_patient_user(db, cpf, name="teste")

    db_user = db.query(User).get(user.id)
    assert db_user.cpf == cpf

    assert auth.verify_password(password, db_user.password)

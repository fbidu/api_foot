"""
Testes unitários para as funções de banco de dados
"""
from sqlalchemy.orm import Session

from api_pezao import crud
from api_pezao.models import User


def test_find_user_by_email(db: Session):
    """
    Testa se conseguimos encontrar um usuário por email
    """

    user = User(email="test@local")
    db.add(user)
    db.commit()

    found_user = crud.find_user(db, email="test@local")

    assert found_user
    assert user == found_user


def test_find_user_by_cpf(db: Session):
    """
    Testa se conseguimos encontrar um usuário por cpf
    """

    user = User(email="test@local", cpf="00000000000")
    db.add(user)
    db.commit()

    found_user = crud.find_user(db, cpf="00000000000")

    assert found_user
    assert user == found_user

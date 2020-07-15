"""
Utilitários para testes que interagem com o banco de dados
"""
from sqlalchemy.orm import Session

from api_pezao.crud import create_user
from api_pezao.models import User
from api_pezao.schemas import UserCreate


def create_test_user(
    db: Session,
    email="test@test.com",
    cpf="00000000000",
    password="secret",
    name="test",
) -> User:
    """
    Cria um usuário de testes dentro do banco de dados
    """
    user = UserCreate(email=email, cpf=cpf, password=password, name=name)
    user = create_user(db, user)

    return user

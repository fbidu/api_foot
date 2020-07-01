"""
Utilitários para testes que interagem com o banco de dados
"""
from sqlalchemy.orm import Session

from api_pezao.models import User


def create_test_user(
    db: Session, email="test@test", cpf="00000000000", password="secret"
) -> User:
    """
    Cria um usuário de testes dentro do banco de dados
    """
    user = User(email=email, cpf=cpf, password=password)
    db.add(user)
    db.commit()

    return user

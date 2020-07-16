"""
Testes unitários para autenticação
"""
from api_pezao import auth

from .db_utils import create_test_user


def test_verify_password():
    """
    Testa se a verificação de senha funciona
    """
    hashed_password = auth.get_password_hash("teste123")

    assert auth.verify_password("teste123", hashed_password)


def test_authenticate_user(db):
    """
    Testa se a autenticação de um usuário
    por e-mail e senha funciona
    """
    user = create_test_user(db, password="123")
    assert auth.verify_password("123", user.password)

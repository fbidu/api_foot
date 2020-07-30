"""
Testes funcionais para usuários

Testam contra uma API em modo de teste se as operações com usuários funcionam
"""

from ..utils import create_demo_user


def test_create_user(client):
    """
    Testa se é possível criar um usuário
    """

    response = create_demo_user(client)
    assert response.status_code == 201

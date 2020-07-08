"""
Testes funcionais para autenticação
"""
from enum import auto
from fastapi.testclient import TestClient
from pytest import fixture

from api_pezao.models import User

from ..db_utils import create_test_user
from ..utils import log_user_in


@fixture
def test_user(db):
    """
    Oferece um usuário de teste
    """
    return create_test_user(db, password="secret")


class TestAuth:
    """
    Class que testa vários pontos do mecanismo de autenticação
    """

    @fixture(autouse=True)
    def __test_user(self, db):
        """
        Oferece um usuário de teste
        """
        self.test_user = create_test_user(db, password="secret")

    @fixture(autouse=True)
    def _test_client(self, client):
        """
        Oferece um cliente de teste da API
        """
        self.client = client

    def test_login_accepts_email(self):
        """
        Testa se o endpoint de login funciona com o e-mail do usuário
        """
        payload = {"username": self.test_user.email, "password": "secret"}

        response = log_user_in(client=self.client, **payload)

        assert response.status_code == 200

        data = response.json()

        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    # pylint: disable=unused-argument
    def test_invalid_email_fails(self):
        """
        Checa se um usuário com senha válida mas email errado falha
        """
        payload = {"username": "invalid!!", "password": "secret"}

        response = log_user_in(client=self.client, **payload)

        assert response.status_code == 401


def test_invalid_password_fails(client: TestClient, test_user: User):
    """
    Checa se um usuário com email válido mas senha inválida falha
    """
    payload = {"username": test_user.email, "password": "invalid!!"}

    response = log_user_in(client=client, **payload)

    assert response.status_code == 401

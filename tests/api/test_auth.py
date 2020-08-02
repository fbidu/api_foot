"""
Testes funcionais para autenticação
"""
from datetime import datetime
from fastapi.testclient import TestClient
from jose import jwt
from pytest import fixture, approx
from sqlalchemy.orm.session import Session

from api_pezao.models import User

from ..db_utils import create_test_user, create_super_user
from ..utils import auth_header, log_user_in


class TestAuth:
    """
    Classe que testa vários pontos do mecanismo de autenticação
    """

    root: User
    test_user: User
    client: TestClient

    @fixture(autouse=True)
    def __test_user(self, db: Session):
        """
        Oferece um usuário de teste
        """
        self.test_user = create_test_user(db, password="secret")
        self.root = create_super_user(db, cpf="123456789", email="root@root.com")

    @fixture(autouse=True)
    def _test_client(self, client: TestClient):
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

        token = data["access_token"]
        claims = jwt.get_unverified_claims(token)
        assert "sub" in claims
        assert claims["sub"] == self.test_user.email

    # pylint: disable=unused-argument
    def test_invalid_email_fails(self):
        """
        Checa se um usuário com senha válida mas email errado falha
        """
        payload = {"username": "invalid!!", "password": "secret"}

        response = log_user_in(client=self.client, **payload)

        assert response.status_code == 401

    def test_invalid_password_fails(self):
        """
        Checa se um usuário com email válido mas senha inválida falha
        """
        payload = {"username": self.test_user.email, "password": "invalid!!"}

        response = log_user_in(client=self.client, **payload)

        assert response.status_code == 401

    def test_login_accepts_cpf(self):
        """
        Testa se o endpoint de login funciona com o cpf do usuário
        """
        payload = {"username": self.test_user.cpf, "password": "secret"}

        response = log_user_in(client=self.client, **payload)

        assert response.status_code == 200

        data = response.json()

        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_me(self):
        """
        There should be a /me endpoint that
        returns info on the logged in user
        """
        response = self.client.get("/users/me/", headers=auth_header(self.client))
        assert response.status_code == 200

        user_data = response.json()

        assert "id" in user_data
        assert "password" not in user_data
        assert "email" in user_data

    def test_me_without_token_fails(self):
        """
        There should be a /me endpoint that
        returns info on the logged in user
        """
        response = self.client.get(
            "/users/me/", headers={"authorization": "Bearer poteitou"}
        )
        assert response.status_code == 401

    def test_superuser_login_has_longer_token(self):
        """
        Super users need longer tokens for UX reasons
        """

        payload = {"username": self.root.email, "password": "secret"}

        response = log_user_in(client=self.client, **payload)

        assert response.status_code == 200

        token = response.json()["access_token"]

        token_exp = jwt.get_unverified_claims(token)["exp"]
        now = datetime.timestamp(datetime.now())

        assert (token_exp - now) == approx(12 * 60 * 60, abs=10)

        assert token

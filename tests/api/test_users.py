"""
Testes funcionais para usuários
"""
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session

from api_pezao.models import User

from ..db_utils import create_test_user
from ..utils import create_demo_user, auth_header


class TestClientPezao:
    """
    Classe que testa vários pontos do mecanismo de autenticação
    """

    test_user: User
    client: TestClient

    @fixture(autouse=True)
    def __test_user(self, db: Session):
        """
        Oferece um usuário de teste
        """
        self.test_user = create_test_user(db, password="secret", is_superuser=True)

    @fixture(autouse=True)
    def _test_client(self, client: TestClient):
        """
        Oferece um cliente de teste da API
        """
        self.client = client
        self.client.headers = auth_header(client)

    def test_create_user(self):
        """
        Testa se é possível criar um usuário
        """

        response = create_demo_user(
            self.client, cpf="11111111111", email="test2@test.com"
        )
        assert response.status_code == 201

    def test_list_user(self):
        """
        Testa se conseguimos listar usuários
        """
        response = self.client.get("/users/")
        assert response.status_code == 200

"""
Testes funcionais para usuários
"""
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session

from api_pezao.auth import verify_password
from api_pezao.crud import find_user
from api_pezao.deps import get_settings
from api_pezao.models import User

from ..db_utils import create_test_user
from ..utils import assert_response_matches_payload, auth_header, create_demo_user


class TestClientPezao:
    """
    Classe que testa vários pontos do mecanismo de autenticação
    """

    test_user: User
    db: Session
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

    @fixture(autouse=True)
    def _db(self, db: Session):
        """
        Banco de testes
        """
        self.db = db

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

    def test_delete_user(self):
        """
        Testa se um super usuário pode performar soft-delete em outro
        """
        user_to_delete = create_demo_user(
            self.client, cpf="99999999999", email="user@todelete.com"
        )

        user_id = user_to_delete.json()["id"]

        response = self.client.delete(f"/users/{user_id}")

        assert response.status_code == 200

        deleted_user = response.json()

        assert not find_user(self.db, deleted_user["cpf"])
        assert not find_user(self.db, deleted_user["email"])

        assert self.db.query(User).get(deleted_user["id"])

    def test_create_superuser_with_token(self):
        """
        Usando o shared secret, uma pessoa pode criar um superuser
        """
        headers = {"authorization": get_settings().upload_secret}

        payload = {
            "cpf": "12345678900",
            "name": "A",
            "email": None,
            "login": "aaaaaa",
            "is_superuser": True,
            "is_staff": False,
            "password": "a",
        }

        response = self.client.post("/users/", json=payload, headers=headers)

        assert response.status_code == 201

        password = payload.pop("password")
        assert_response_matches_payload(response, payload, expected_status=201)

        db_user = find_user(self.db, username=payload["cpf"])
        assert db_user

        assert verify_password(password, db_user.password)
        assert db_user.is_superuser

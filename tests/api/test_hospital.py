"""
Testes funcionais para um hospital
"""
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session

from api_pezao.crud.hospital import read_hospitals
from api_pezao.models import HospitalCS, User
from ..utils import (
    auth_header,
    create_demo_hospital,
    create_demo_user,
    assert_payload_in_database,
    assert_response_matches_payload,
    assert_json_matches_payload,
)


class TestHospital:
    """
    Classe para testes funcionais de hospital
    """

    test_user: User
    client: TestClient
    db: Session
    payload: dict
    test_hospital: HospitalCS

    @fixture(autouse=True)
    def __test_user(self, client):
        """
        Oferece um usuário de teste
        """
        self.test_user = create_demo_user(client, password="secret")

    @fixture(autouse=True)
    def _test_client(self, client: TestClient):
        """
        Oferece um cliente de teste da API
        """
        self.client = client
        self.client.headers = auth_header(self.client)

    @fixture(autouse=True)
    def _db(self, db: Session):
        """
        Banco de testes
        """
        self.db = db

    @fixture(autouse=True)
    def _test_hospital(self):
        self.payload = {
            "code": "TEST_HC",
            "name": "test hosp",
            "type_": "CS",
            "email1": "testhosp1@test.com",
            "email2": "testhosp2@test.com",
            "email3": "testhosp3@test.com",
        }
        response = create_demo_hospital(self.client, **self.payload)

        id_ = response.json()["id"]
        self.payload["type"] = self.payload.pop("type_")

        self.test_hospital = (
            self.db.query(HospitalCS).filter(HospitalCS.id == id_).first()
        )

    def test_create_hospital_works(self):
        """
        Testa se conseguimos criar um hospital
        """
        payload = {
            "code": "TEST_HC1",
            "name": "test hosp1",
            "type_": "CS",
            "email1": "testhosp11@test.com",
            "email2": "testhosp21@test.com",
            "email3": "testhosp31@test.com",
        }
        response = create_demo_hospital(self.client, **payload)

        payload["type"] = payload.pop("type_")
        assert_response_matches_payload(response, payload)
        assert_payload_in_database(
            self.db, payload, HospitalCS, "id", response.json()["id"]
        )

    def test_create_hospital_unlogged_does_not_work(self):
        """
        Usuários anônimos não podem criar hospitais
        """
        client_ = self.client
        client_.headers = {}
        response = create_demo_hospital(client_)

        assert response.status_code == 401

    def _test_read_hospital(self, args=""):
        """
        Testa se a leitura de hospitais funciona
        """
        response = self.client.get(f"/hospitals/?{args}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        hospital = data[0]
        assert_json_matches_payload(hospital, self.payload)

    def test_read_hospital_unlogged_does_not_work(self):
        """
        Usuários anônimos não podem criar hospitais
        """
        client_ = self.client
        client_.headers = {}
        response = self.client.get("/hospitals/")

        assert response.status_code == 401

    def test_read_all_hospitals(self):
        """
        Testa se a leitura de hospitais funciona
        """
        self._test_read_hospital()

    def test_read_hospitals_by_code(self):
        """
        Testa se a leitura de hospital por código funciona
        """
        self._test_read_hospital(f"code={self.test_hospital.code}")

    def test_read_hospitals_by_name(self):
        """
        Testa se a leitura de hospital por código funciona
        """
        self._test_read_hospital(f"name={self.test_hospital.name}")

    def test_read_hospitals_by_email(self):
        """
        Testa se a leitura de hospital por código funciona
        """
        self._test_read_hospital(f"email={self.test_hospital.email1}")
        self._test_read_hospital(f"email={self.test_hospital.email2}")
        self._test_read_hospital(f"email={self.test_hospital.email3}")

    def test_update_hospital(self):
        """
        Testa se a atualização de um hospital funciona
        """

        payload = {
            "code": "TEST_HC_novo",
            "name": "test hosp_novo",
            "type": "CS_novo",
            "email1": "testhosp1@test.com_novo",
            "email2": "testhosp2@test.com_novo",
            "email3": "testhosp3@test.com_novo",
        }

        response = self.client.put(f"/hospitals/{self.test_hospital.id}/", json=payload)

        assert response.status_code == 200
        assert_response_matches_payload(response, payload)

    def test_delete_hospital(self):
        """
        Testa se a deleção de um hospital funciona
        """

        response = self.client.delete(f"/hospitals/{self.test_hospital.id}/")

        assert response.status_code == 200
        deleted_hospital = response.json()

        # Testa se a deleção foi soft

        # 1. O hospital não deve aparecer mais numa busca comum
        assert len(read_hospitals(self.db)) == 0

        # 2. Mas o hospital ainda deve estar presente
        query = self.db.query(HospitalCS).all()

        assert len(query) == 1
        assert query[0].id == deleted_hospital["id"]
        assert query[0].code == deleted_hospital["code"]

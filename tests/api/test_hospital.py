"""
Testes funcionais para um hospital
"""
from api_pezao.models import HospitalCS
from ..utils import (
    create_demo_hospital,
    create_demo_user,
    assert_payload_in_database,
    assert_response_matches_payload,
)


def test_create_hospital_works(client, db):
    """
    Testa se conseguimos criar um hospital
    """
    payload = {
        "code": "TEST_HC",
        "name": "test hosp",
        "type_": "CS",
        "email1": "testhosp1@test.com",
        "email2": "testhosp2@test.com",
        "email3": "testhosp3@test.com",
    }
    create_demo_user(client)
    response = create_demo_hospital(client, **payload)

    payload["type"] = payload.pop("type_")
    assert_response_matches_payload(response, payload)
    assert_payload_in_database(db, payload, HospitalCS, "id", response.json()["id"])

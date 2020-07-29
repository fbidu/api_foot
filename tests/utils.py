"""
Utilitary function to aid testing
"""
from typing import Any
from requests import Response
from sqlalchemy.orm.session import Session
from api_pezao.utils import sha256


def check_files_equal(path_a, path_b):
    """
    Checks if two files are equal
    """

    return sha256(path_a) == sha256(path_b)


def post_pdf(sample_pdf, client) -> Response:
    """
    Posts a file to the main PDF endpoint
    """
    files = {"pdf_file": open(sample_pdf, "rb")}
    return client.post("/pdf/", files=files)


def create_demo_user(
    client, cpf="00000000000", email="test@test.com", password="secret", super_user=True
) -> Response:
    """
    Creates a user for testing purposes
    """
    payload = {
        "cpf": cpf,
        "name": "Teste",
        "email": email,
        "password": password,
        "is_superuser": super_user,
    }

    response = client.post("/users/", json=payload)
    return response


def log_user_in(client, username, password) -> Response:
    """
    Authenticates an user and returns a token
    """
    payload = {"username": username, "password": password}
    return client.post("/token", data=payload)


def auth_header(client, username="test@test.com", password="secret") -> Response:
    """
    Returns a dict containing the authorization header for a given user
    """
    token = log_user_in(client, username, password).json()["access_token"]
    return {"authorization": f"Bearer {token}"}


# pylint: disable=too-many-arguments
def create_demo_hospital(
    client,
    code="TEST_HC",
    name="test hosp",
    type_="CS",
    email1="testhosp1@test.com",
    email2="testhosp2@test.com",
    email3="testhosp3@test.com",
    username="test@test.com",
    password="secret",
):
    """
    Cria um hospital de teste
    """
    payload = {
        "code": code,
        "name": name,
        "type": type_,
        "email1": email1,
        "email2": email2,
        "email3": email3,
        "password": password,
    }

    return client.post(
        "/hospitals/", json=payload, headers=auth_header(client, username, password)
    )


def assert_response_matches_payload(response, payload, expected_status=200):
    """
    Helper function to ease checking if a given JSON Response matches an
    input payload that was given to it.

    This function expects that the response's JSON contains at least ALL
    the fields defined on the payload
    """
    assert response.status_code == expected_status

    data = response.json()
    assert_json_matches_payload(data, payload)


def assert_json_matches_payload(json: dict, payload: dict):
    """
    Checks if a given JSON object contains at least all the keys
    in a given payload and if their values match
    """
    for key, value in payload.items():
        assert key in json, f"Key '{key}' not present in the response"
        assert json[key] == value, f"Value for '{key}' does not match"


def assert_payload_in_database(
    db: Session, payload: dict, model, key: str, key_value: Any
):
    """
    Assert if a given JSON Payload is present in the db, inside the given model.
    The key argument and value should refer to that model's primary key
    """

    db_entity = db.query(model).filter(getattr(model, key) == key_value).first()

    assert db_entity

    for key_, value in payload.items():
        assert hasattr(db_entity, key_), f"Key '{key_}' not present in the response"
        assert getattr(db_entity, key_) == value, f"Value for '{key_}' does not match"

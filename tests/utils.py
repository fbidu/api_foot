"""
Utilitary function to aid testing
"""
from requests import Response
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

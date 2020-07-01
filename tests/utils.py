"""
Utilitary function to aid testing
"""
from api_pezao.utils import sha256


def check_files_equal(path_a, path_b):
    """
    Checks if two files are equal
    """

    return sha256(path_a) == sha256(path_b)


def post_pdf(sample_pdf, client):
    """
    Posts a file to the main PDF endpoint
    """
    files = {"pdf_file": open(sample_pdf, "rb")}
    return client.post("/pdf/", files=files)


def create_demo_user(
    client, cpf="00000000000", email="teste@teste.com", password="secret"
):
    """
    Creates a user for testing purposes
    """
    payload = {"cpf": cpf, "name": "Teste", "email": email, "password": password}

    response = client.post("/users/", json=payload)
    return response


def log_user_in(username, password, client):
    """
    Authenticates an user and returns a token
    """
    payload = {"username": username, "password": password}
    client.post("/login", data=payload)

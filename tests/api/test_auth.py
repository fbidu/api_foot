"""
Testes funcionais para autenticação
"""
from fastapi.testclient import TestClient
from ..utils import create_demo_user


def test_login_accepts_email(client: TestClient):
    """
    Testa se o endpoint de login funciona com o e-mail do usuário
    """
    email = "login@test.com"
    password = "login_test"
    create_demo_user(client, email=email, password=password)

    payload = {"username": email, "password": password}

    response = client.post("/token", data=payload)

    assert response.status_code == 200

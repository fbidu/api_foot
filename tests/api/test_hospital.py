"""
Testes funcionais para um hospital
"""
from ..utils import create_demo_hospital, create_demo_user


def test_create_hospital_works(client):
    """
    Testa se conseguimos criar um hospital
    """
    create_demo_user(client)
    response = create_demo_hospital(client)

    assert response.status_code == 200

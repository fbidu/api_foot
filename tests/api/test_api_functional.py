"""
Testes funcionais - determinam se o comportamento dos endpoints é o esperado
"""


def test_root(client):
    """
    Testa se um GET em / funciona
    """
    response = client.get("/")
    assert response.status_code == 200

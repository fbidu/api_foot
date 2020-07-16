"""
Testa a raíz da aplicação
"""


def test_root(client):
    """
    Testa se um GET em / funciona
    """
    response = client.get("/")
    assert response.status_code == 200

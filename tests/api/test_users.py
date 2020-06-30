"""
Testes funcionais para usuários

Testam contra uma API em modo de teste se as operações com usuários funcionam
"""


def test_create_user(client):
    """
    Testa se é possível criar um usuário
    """

    payload = {
        "cpf": "00000000000",
        "name": "Teste",
        "email": "teste@teste.com",
        "password": "secret",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

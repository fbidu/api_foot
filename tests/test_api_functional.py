"""
Testes funcionais - determinam se o comportamento dos endpoints é o esperado
"""
from pathlib import Path
from fastapi.testclient import TestClient
from api_pezao.main import app

client = TestClient(app)


def test_root():
    """
    Testa se um GET em / funciona
    """
    response = client.get("/")
    assert response.status_code == 200

def test_post_csv():
    """
    Testa se o envio de um arquivo para /csv retorna o número de linhas nele
    """
    sample_file = Path("tests/demo.csv").absolute()
    files = {"file": open(sample_file, "r")}
    response = client.post("/csv/", files=files)

    assert response.status_code == 200
    assert response.json()

    content =  response.json()

    assert content["lines"] == 4

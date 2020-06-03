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
    files = {"csv_file": open(sample_file, "r")}
    response = client.post("/csv/", files=files)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content["lines"] == 4


def test_post_pdf():
    """
    Testa se o envio de um arquivo para /pdf retorna o nome e tamanho dele
    """
    sample_file = Path("tests/demo.pdf").absolute()
    files = {"pdf_file": open(sample_file, "rb")}
    response = client.post("/pdf/", files=files)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content == 10453

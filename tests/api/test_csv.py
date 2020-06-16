"""
Testes funcionais para envio de PDF
"""
from pathlib import Path


def test_post_csv(client):
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

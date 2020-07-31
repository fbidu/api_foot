"""
Testes funcionais para envio de PDF
"""
from pathlib import Path

from api_pezao.crud.result import read_results
from api_pezao.deps import get_settings


def test_post_csv_requires_token(client):
    """
    CSV exige um token
    """
    sample_file = Path("tests/demo.csv").absolute()
    files = {"csv_file": open(sample_file, "r")}
    response = client.post("/csv/", files=files)
    assert response.status_code == 401


def test_post_csv(client, db):
    """
    Testa se o envio de um arquivo para /csv retorna o número de linhas nele
    """
    header = {"authorization": get_settings().upload_secret}
    sample_file = Path("tests/demo.csv").absolute()
    files = {"csv_file": open(sample_file, "r")}
    response = client.post("/csv/", files=files, headers=header)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content["lines"] == 159

    db_results = read_results(db)
    assert len(db_results) == 159

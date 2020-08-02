"""
Testes funcionais para envio de PDF
"""
from pathlib import Path

from api_pezao.crud.result import read_results
from api_pezao.deps import get_settings
from api_pezao.models import TemplatesResult, HospitalCS

from ..test_csv_input import import_test_results


def test_post_csv_requires_token(client):
    """
    CSV exige um token
    """
    sample_file = Path("tests/demo.csv").absolute()
    files = {"csv_file": open(sample_file, "r")}
    response = client.post("/csv/?type=results", files=files)
    assert response.status_code == 401


def test_post_results_csv(client, db):
    """
    Testa se o envio de um arquivo para /csv retorna o número de linhas nele
    """
    header = {"authorization": get_settings().upload_secret}
    sample_file = Path("tests/demo.csv").absolute()
    files = {"csv_file": open(sample_file, "r")}
    response = client.post("/csv/?type=results", files=files, headers=header)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content["lines"] == 40

    db_results = read_results(db)
    assert len(db_results) == 40


def test_post_templates_results_csv(client, db):
    """
    Testa se o envio de um arquivo para /csv retorna o número de linhas nele
    """
    header = {"authorization": get_settings().upload_secret}
    sample_file = Path("tests/demo_templates_result.csv").absolute()
    files = {"csv_file": open(sample_file, "r")}
    results = import_test_results(db)
    response = client.post("/csv/?type=templates_results", files=files, headers=header)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content["lines"] == 40

    db_objects = db.query(TemplatesResult).all()
    assert len(db_objects) == 40

    template_sms_0 = db_objects[0]

    assert template_sms_0.template_id == 1
    assert template_sms_0.IDExport == results[0].IDExport
    assert template_sms_0.result.IDExport == results[0].IDExport


def test_post_hospitals_csv(client, db):
    """
    Testa se o envio de um arquivo para /csv de hospital funciona
    """
    header = {"authorization": get_settings().upload_secret}
    sample_file = Path("tests/demo_hospital.csv").absolute()
    files = {"csv_file": open(sample_file, "r")}

    response = client.post("/csv/?type=hospitals", files=files, headers=header)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content["lines"] == 2

    db_objects = db.query(HospitalCS).all()
    assert len(db_objects) == 2

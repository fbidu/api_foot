"""
Testes funcionais - determinam se o comportamento dos endpoints é o esperado
"""
from datetime import datetime
from os import mkdir, rmdir, remove
from pathlib import Path
from fastapi.testclient import TestClient
from pytest import fixture

from api_pezao import config, main

from .utils import check_files_equal, post_pdf

client = TestClient(main.app)

# pylint: disable=redefined-outer-name
@fixture
def sample_pdf():
    """
    Provides the full path for a sample pdf file
    """
    return Path("tests/demo.pdf").absolute()


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


def test_post_pdf(sample_pdf):
    """
    Testa se o envio de um arquivo para /pdf retorna o tamanho dele e salva
    """
    response = post_pdf(sample_pdf, client)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content == 10453
    assert Path("/tmp/demo.pdf").exists()
    assert check_files_equal(sample_pdf, "/tmp/demo.pdf")


def test_post_pdf_obeys_env(sample_pdf):
    """
    Testa se ao enviar um arquivo para /pdf, ele é
    salvo em um lugar especificado
    """
    now = int(datetime.timestamp(datetime.now()))
    target_folder = f"/tmp/pdf_demo_{now}"
    mkdir(target_folder)

    target_path = Path(target_folder)
    target_file = target_path.joinpath(sample_pdf.name)

    assert target_path.exists(), "Falha ao criar pasta para testar envio de PDF!"

    settings = config.Settings(pdf_storage_path=str(target_path.absolute()))
    main.app.dependency_overrides[main.get_settings] = lambda: settings

    response = post_pdf(sample_pdf, client)

    assert response.status_code == 200
    assert target_file.exists()
    assert check_files_equal(sample_pdf, target_file)

    remove(target_file)
    rmdir(target_path)
    assert not target_path.exists()

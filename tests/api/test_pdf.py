"""
Testes funcionais para POST de PDF
"""
from datetime import datetime
from os import mkdir, remove, rmdir
from pathlib import Path
from pytest import fixture

from api_pezao import config, main

from ..utils import post_pdf, check_files_equal


# pylint: disable=redefined-outer-name
@fixture
def sample_pdf():
    """
    Provides the full path for a sample pdf file
    """
    return Path("tests/demo.pdf").absolute()


def test_post_pdf(client, sample_pdf):
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


def test_post_pdf_obeys_env(client, sample_pdf):
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

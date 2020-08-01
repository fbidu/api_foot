"""
Testes funcionais para POST de PDF
"""

from datetime import datetime
from os import mkdir, remove, rmdir
from pathlib import Path
from pytest import fixture


from api_pezao import config, main
from api_pezao import deps
from api_pezao.models.result import Result
from api_pezao.crud import create_patient_user
from api_pezao.schemas import ResultCreate
from api_pezao.utils import sha256

from ..utils import auth_header, post_pdf, check_files_equal


# pylint: disable=redefined-outer-name
@fixture
def sample_pdf():
    """
    Provides the full path for a sample pdf file
    """
    return Path("tests/demo.pdf").absolute()


def test_post_pdf(client, sample_pdf: Path):
    """
    Testa se o envio de um arquivo para /pdf retorna o tamanho dele e salva
    """
    response = post_pdf(sample_pdf, client)

    assert response.status_code == 200
    assert response.json()

    content = response.json()

    assert content["length"] == 10453
    assert content["sha256"] == sha256(sample_pdf)
    assert content["filename"] == sample_pdf.name

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
    main.app.dependency_overrides[deps.get_settings] = lambda: settings

    response = post_pdf(sample_pdf, client)

    assert response.status_code == 200
    assert target_file.exists()
    assert check_files_equal(sample_pdf, target_file)

    remove(target_file)
    rmdir(target_path)
    assert not target_path.exists()

    del main.app.dependency_overrides[deps.get_settings]


def test_result_contains_full_pdf_path(client, db, sample_pdf):
    """
    Testa se o usuário logado consegue pegar seus resultados
    """

    result = ResultCreate(
        IDExport=1, DNV=1, CNS=1, CPF="00000000000", PDF_Filename="demo.pdf"
    )
    result2 = ResultCreate(
        IDExport=2, DNV=2, CNS=2, CPF="00000011000", PDF_Filename="demo1.pdf"
    )
    db_result = Result(**result.dict())
    db.add(db_result)
    db.add(Result(**result2.dict()))
    db.commit()
    db.refresh(db_result)

    assert db_result
    post_pdf(sample_pdf, client)

    _, password = create_patient_user(db, db_result.CPF, "teste")
    auth_headers = auth_header(client, username=db_result.CPF, password=password)
    results = client.get("/results/", headers=auth_headers)

    assert results.status_code == 200

    data = results.json()
    assert len(data) == 1
    result = data[0]

    result_pdf = client.get("/pdf/demo.pdf", headers=auth_headers)
    assert result_pdf.status_code == 200

    wrong_pdf = client.get("/pdf/demo1.pdf", headers=auth_headers)
    assert wrong_pdf.status_code == 404

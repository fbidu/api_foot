"""
Files router
"""

from enum import Enum
from pathlib import Path

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import config, log, sms_utils
from ..auth import oauth2_scheme
from ..crud import create_patient_user, get_current_user, read_results
from ..csv_input import (
    import_hospitals_csv,
    import_results_csv,
    import_templates_results_csv,
)
from ..deps import get_db, get_settings
from ..pdf_input import save_pdf
from ..schemas.pdf_processed import PDFProcessed
from ..utils import sha256

router = APIRouter()


class CSVTypes(str, Enum):
    """
    Tipos de CSV aceitos para importação
    """

    results = "results"
    templates_results = "templates_results"
    hospitals = "hospitals"


# pylint: disable=redefined-builtin
@router.post("/csv/")
def read_csv(
    type: CSVTypes,
    csv_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    settings: config.Settings = Depends(get_settings),
):
    """
    Receives a CSV input file
    """
    if authorization != settings.upload_secret:
        raise HTTPException(401, "Operação inválida!")

    lines = 0

    with csv_file.file as file:
        content = file.read()
        content = content.decode("utf-8")
        content = content.split("\n")
        if type == CSVTypes.results:
            lines = len(import_results_csv(content, db))
        elif type == CSVTypes.templates_results:
            lines = len(import_templates_results_csv(content, db))
        elif type == CSVTypes.hospitals:
            lines = len(import_hospitals_csv(content, db))
        else:
            raise HTTPException(400)

    log("[CSV] CSV foi importado.", db)

    return {"lines": lines}


@router.post("/pdf/", response_model=PDFProcessed)
def read_pdf(
    pdf_file: UploadFile = File(...),
    settings: config.Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Receives and stores a PDF file. The location of the file will be determined
    by the `pdf_storage_path` config.
    """
    if authorization != settings.upload_secret:
        raise HTTPException(401, "Operação inválida!")

    file = pdf_file.file
    content = file.read()

    # Builds the path
    target_path = Path(settings.pdf_storage_path)
    filename = target_path.joinpath(pdf_file.filename)
    save_pdf(content, filename)

    db_results = read_results(db, PDF_Filename=pdf_file.filename)

    if db_results:
        db_result = db_results[0]
        user, password = create_patient_user(
            db,
            cpf=db_result.CPF,
            name=f"{db_result.prMotherFirstname} {db_result.prMotherSurname}",
        )

        sms_message = f"{user.name}, o resultado do exame do pézinho está pronto. "

        if password:
            sms_message += f"Faça login com seu cpf e a senha {password}"

        number = db_result.ptnPhone1 or db_result.ptnPhone2

        if number:
            sms_utils.send_sms(number, sms_message)
        else:
            log(
                f"[PDF] Arquivo {pdf_file.filename} importado mas sem "
                "celulares associados. SMS não será enviado."
            )
    else:
        log(
            f"[PDF] Arquivo {pdf_file.filename} importado mas sem "
            "resultado associado. SMS não será enviado."
        )

    log("[PDF] PDF foi importado.", db)

    return PDFProcessed(
        length=len(content), filename=pdf_file.filename, sha256=sha256(filename)
    )


@router.get("/pdf/{file_name}")
def return_pdf(
    file_name: str,
    settings: config.Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Retorna o pdf do resultado
    """
    logged_user = get_current_user(db, token)

    if not logged_user:
        raise HTTPException(403)

    if not (logged_user.is_staff or logged_user.is_superuser):
        results = read_results(db, cpf=logged_user.cpf, PDF_Filename=file_name)
        if not results:
            raise HTTPException(404)

    result_path = Path(settings.pdf_storage_path).joinpath(file_name)

    return FileResponse(str(result_path.absolute()), media_type="application/pdf")

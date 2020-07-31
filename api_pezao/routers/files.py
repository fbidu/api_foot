"""
Files router
"""

from enum import Enum
from pathlib import Path

from fastapi import Depends, File, UploadFile, APIRouter, Header, HTTPException
from sqlalchemy.orm import Session

from .. import config, log
from ..csv_input import import_results_csv, import_templates_results_csv

from ..pdf_input import save_pdf
from ..schemas.pdf_processed import PDFProcessed
from ..utils import sha256
from ..deps import get_db, get_settings

router = APIRouter()


class CSVTypes(str, Enum):
    """
    Tipos de CSV aceitos para importação
    """

    results = "results"
    templates_results = "templates_results"
    hospitals = "hospitals"


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

    log("[CSV] CSV foi importado.", db)

    return {"lines": lines}


@router.post("/pdf/", response_model=PDFProcessed)
def read_pdf(
    pdf_file: UploadFile = File(...),
    settings: config.Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):
    """
    Receives and stores a PDF file. The location of the file will be determined
    by the `pdf_storage_path` config.
    """
    file = pdf_file.file
    content = file.read()

    # Builds the path
    target_path = Path(settings.pdf_storage_path)
    filename = target_path.joinpath(pdf_file.filename)

    save_pdf(content, filename)

    log("[PDF] PDF foi importado.", db)

    return PDFProcessed(
        length=len(content), filename=pdf_file.filename, sha256=sha256(filename)
    )

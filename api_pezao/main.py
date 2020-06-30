"""
Here be awesome code!
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session


from . import config, crud, schemas
from .csv_input import import_csv
from .database import SessionLocal, engine, Base
from .pdf_input import save_pdf
from .schemas.pdf_processed import PDFProcessed
from .utils import sha256


Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


@lru_cache()
def get_settings():
    """
    Returns a new instance of settings
    """
    return config.Settings()


# Dependency
def get_db():
    """
    Returns a new DB instance
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # pylint: disable=no-member


@app.get("/")
def home():
    """
    The root of the API
    """
    return "Hello, world!"


@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Receives a new user record in `user` and creates
    a new user in the current database
    """
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    """
    Lists all users
    """
    return crud.list_users(db)


@app.post("/csv/")
def read_csv(csv_file: UploadFile = File(...)):
    """
    Receives a CSV input file
    """
    with csv_file.file as file:
        content = file.read()
        content = content.decode("utf-8")
        content = content.split("\n")
        lines = import_csv(content)

    return {"lines": lines}


@app.post("/pdf/", response_model=PDFProcessed)
def read_pdf(
    pdf_file: UploadFile = File(...), settings: config.Settings = Depends(get_settings)
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
    return PDFProcessed(
        length=len(content), filename=pdf_file.filename, sha256=sha256(filename)
    )

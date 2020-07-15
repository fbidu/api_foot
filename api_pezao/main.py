"""
Here be awesome code!
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import config, crud, schemas
from .auth import get_current_user, oauth2_scheme, verify_password
from .csv_input import import_csv
from .database import SessionLocal, engine, Base
from .pdf_input import save_pdf
from .schemas import User
from .schemas.pdf_processed import PDFProcessed
from .utils import sha256, is_valid_cpf, is_valid_email


Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


@lru_cache()
def get_settings():
    """
    Returns a new instance of settings
    """
    return config.Settings()


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


@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, email=form_data.username)
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, cpf=form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}


@app.get("/users/token")
def read_token(token: str = Depends(oauth2_scheme)):
    """
    Dado um `token` retorna informações sobre ele.
    """
    return {"token": token}


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Retorna informações do usuário logado atualmente.
    """
    return current_user


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

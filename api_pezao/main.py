"""
Here be awesome code!
"""
from typing import List

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session


from . import crud, models, schema, settings
from .csv_input import import_csv
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

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


@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """
    Receives a new user record in `user` and creates
    a new user in the current database
    """
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schema.User])
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


@app.post("/pdf/")
def read_pdf(pdf_file: UploadFile = File(...)):
    """
    Receives and stores a PDF file
    """
    content = pdf_file.file.read()
    return len(content)

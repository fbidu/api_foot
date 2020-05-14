"""
Here be awesome code!
"""
from typing import List

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session


from . import crud, models, schema
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
async def read_csv(file: UploadFile = File(...)):
    """
    Receives a CSV input file
    """
    content = open(file.file, "rb")
    lines = import_csv(content)
    return {"lines": lines}

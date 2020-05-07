"""
Here be awesome code!
"""
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session


from . import crud, models, schema
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
        # pylint: disable=no-member
        db.close()


@app.get("/")
def home():
    return "Hello, world!"


@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schema.User])
def read_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

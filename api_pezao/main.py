"""
Here be awesome code!
"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, schemas, log, sms_utils
from .auth import oauth2_scheme
from .database import engine, Base
from .routers import auth, files, hospitals, results, users
from .deps import get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(hospitals.router)
app.include_router(results.router)
app.include_router(users.router)


origins = ["http://localhost:3000", "http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """
    The root of the API
    """
    return "Hello, world!"


@app.get("/logs/", response_model=List[schemas.Log])
def read_logs(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Lista os logs
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        return crud.list_logs(db)

    raise HTTPException(
        status_code=403,
        detail=f"Um usuário ({logged_user.name}) sem permissão tentou ler os logs",
    )


@app.get("/test_get_hospital_user/", response_model=schemas.User)
def test_get_hospital_user(id_: int, db: Session = Depends(get_db)):
    """
    Teste do user de hospital
    """
    return crud.test_get_hospital_user(db, id_)


@app.post("/sms_sweep")
def sms_sweep(
    background_tasks: BackgroundTasks,
    hospitals: List[str] = None,
    db: Session = Depends(get_db),
):
    """
    Envia todos os SMSs pendentes
    """
    background_tasks.add_task(sms_utils.sms_intermediary, hospitals, db)
    return {"message": "SMSs scheduled"}

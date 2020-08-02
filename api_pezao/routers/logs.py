"""
Results router
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..auth import oauth2_scheme
from ..deps import get_db

router = APIRouter()


@router.get("/logs/", response_model=List[schemas.Log])
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

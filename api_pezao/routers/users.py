"""
Rotas para usuários
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from .. import crud, schemas, log
from ..auth import oauth2_scheme
from ..deps import get_db


router = APIRouter()


@router.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Lists all users
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        user_list = crud.list_users(db)

        log(
            f"[LISTA DE USUÁRIOS] Usuários foram listados pelo superuser {logged_user.name}",
            db,
            user_id=logged_user.id,
        )

        return user_list

    log(
        f"[LISTA DE USUÁRIOS] Usuário comum {logged_user.name}, tentou listar usuários!",
        db,
        user_id=logged_user.id,
    )
    raise HTTPException(
        status_code=403, detail="Usuário sem permissão tentou listar usuários"
    )


@router.get("/users/token")
def read_token(token: str = Depends(oauth2_scheme)):
    """
    Dado um `token` retorna informações sobre ele.
    """
    return {"token": token}


@router.get("/users/me", response_model=schemas.User)
def read_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Retorna informações do usuário logado atualmente.
    """
    user = crud.get_current_user(db, token)

    if not user:
        raise HTTPException(401, "Token inválido")

    return user


@router.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Receives a new user record in `user` and creates
    a new user in the current database
    """
    created_user = crud.create_user(db=db, user=user)

    log(
        "[CRIAÇÃO DE USUÁRIO] Usuário criado com "
        f"CPF = {created_user.cpf}, e-mail = {created_user.email}, "
        f"login = {created_user.login}",
        db,
    )

    return created_user


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Deleta um usuário
    """
    logged_user = crud.get_current_user(db, token)
    if not logged_user.is_superuser:
        log(
            f"Usuário {logged_user.name}, que não é superuser, tentou deletar usuário {user_id}!",
            db,
            user_id=logged_user.id,
        )
        raise HTTPException(
            status_code=403, detail="Você não tem permissão para deletar usuários"
        )

    return crud.delete_user(db, user_id)

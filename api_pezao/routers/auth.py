"""
Here be awesome code!
"""
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, log
from ..auth import verify_password, create_access_token
from ..deps import get_db
from ..utils import is_valid_cpf, is_valid_email

router = APIRouter()


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    username = ""

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.email
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.cpf
    else:
        user = crud.find_user(db=db, username=form_data.username)
        username = form_data.username

    if not user:
        log(
            f"[TENTATIVA DE LOGIN] Não existe usuário com e-mail, CPF ou login igual a {form_data.username}",
            db,
        )
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        log(
            f"[TENTATIVA DE LOGIN] Hash da senha fornecida para logar com usuário {form_data.username} não coincide com hash que temos no banco para o usuário {form_data.username} => Senha incorreta!",
            db,
        )
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    log(
        f"[LOGIN] Sucesso: usuário {form_data.username} existe, senhas coincidem, e token de acesso criado para o usuário {form_data.username}",
        db,
    )
    return {
        "access_token": create_access_token({"sub": username}),
        "token_type": "bearer",
    }


@router.post("/token2")
def login2(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    username = ""

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.email
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.cpf
    else:
        user = crud.find_user(db=db, username=form_data.username)
        username = form_data.username

    if not user:
        log(
            f"[TENTATIVA DE LOGIN] Não existe usuário com e-mail, CPF ou login igual a {form_data.username}",
            db,
        )
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        log(
            f"[TENTATIVA DE LOGIN] Hash da senha fornecida para logar com usuário {form_data.username} não coincide com hash que temos no banco para o usuário {form_data.username} => Senha incorreta!",
            db,
        )
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": username})
    log(
        f"[LOGIN] Sucesso: usuário {form_data.username} existe, senhas coincidem, e token de acesso criado para o usuário {form_data.username}",
        db,
    )

    return {"access_token": token, "token_type": "bearer", "user_data": user}


@router.post("/token2_staff_or_admin")
def login2_staff_or_admin(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    username = ""

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.email
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.cpf
    else:
        user = crud.find_user(db=db, username=form_data.username)
        username = form_data.username

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not user.is_staff or (not user.is_superuser):
        raise HTTPException(status_code=401, detail="User is not staff or superuser")

    token = create_access_token({"sub": username})

    return {"access_token": token, "token_type": "bearer", "user_data": user}


@router.post("/token2_family")
def login2_family(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Realiza o login de um usuário aceitando como input um formulário com
    `username` e `password`. O `username` pode ser o e-mail ou CPF de
    um usuário.
    """
    user = None

    username = ""

    if is_valid_email(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.email
    elif is_valid_cpf(form_data.username):
        user = crud.find_user(db=db, username=form_data.username)
        username = user.cpf
    else:
        user = crud.find_user(db=db, username=form_data.username)
        username = form_data.username

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if user.is_staff or user.is_superuser:
        raise HTTPException(status_code=401, detail="User is not family")

    token = create_access_token({"sub": username})

    return {"access_token": token, "token_type": "bearer", "user_data": user}

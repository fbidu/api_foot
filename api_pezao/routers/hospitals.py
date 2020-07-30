"""
Rotas para hospitais
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, log
from ..auth import oauth2_scheme
from ..deps import get_db


router = APIRouter()


@router.get("/hospitals/", response_model=List[schemas.HospitalCS])
def read_hospitals(
    db: Session = Depends(get_db),
    code: str = "",
    name: str = "",
    email: str = "",
    token: str = Depends(oauth2_scheme),
):
    """
    Lista hospitais conforme os filtros. Se o filtro estiver vazio, não é considerado.
    É possível usar operador LIKE no nome do hospital e no e-mail (%).
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        hospital_list = crud.read_hospitals(db, code=code, name=name, email=email)

        log(
            "Hospitais foram buscados com os seguintes filtros: code = %s, name = %s, email = %s, pelo usuário %s"
            % (code, name, email, logged_user.name),
            db,
            user_id=logged_user.id,
        )

        return hospital_list

    log(
        f"Usuário {logged_user.name}, que não é superuser, tentou listar hospitais.",
        db,
        user_id=logged_user.id,
    )
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou listar hospitais"
    )


@router.post("/hospitals/", response_model=schemas.HospitalCS)
def create_hospital(
    hospital: schemas.HospitalCSCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Cria um novo hospital
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        created_hospital = crud.create_hospital(db, hospital)

        log(
            "Novo hospital foi criado com code = %s, type = %s, name = %s, pelo usuário %s"
            % (
                created_hospital.code,
                created_hospital.type,
                created_hospital.name,
                logged_user.name,
            ),
            db,
            user_id=logged_user.id,
        )

        return created_hospital

    log(
        f"Usuário {logged_user.name}, que não é superuser, tentou criar hospital",
        db,
        user_id=logged_user.id,
    )
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou criar hospital"
    )


@router.put("/hospitals/{hospital_id}/", response_model=schemas.HospitalCS)
def update_hospital(
    hospital_id: int,
    hospital: schemas.HospitalCSUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Atualiza um hospital
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        db_hospital = crud.read_hospitals(db, id_=hospital_id)[0]

        if not db_hospital:
            raise HTTPException(status_code=404, detail="Hospital não encontrado")

        updated_hospital = crud.update_hospital(db, db_hospital, hospital)

        log(
            "Um hospital teve dados atualizados: code = %s, type = %s, name = %s, pelo usuário %s"
            % (
                updated_hospital.code,
                updated_hospital.type,
                updated_hospital.name,
                logged_user.name,
            ),
            db,
            user_id=logged_user.id,
        )

        return updated_hospital

    log(
        f"Usuário {logged_user.name}, que não é superuser, tentou atualizar hospital",
        db,
        user_id=logged_user.id,
    )
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou editar hospital"
    )


@router.delete("/hospitals/{hospital_id}/", response_model=bool)
def delete_hospital(
    hospital_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Deleta um hospital
    """
    logged_user = crud.get_current_user(db, token)
    if logged_user.is_superuser:
        db_hospital = crud.read_hospitals(db, id_=hospital_id)[0]

        if not db_hospital:
            raise HTTPException(status_code=404, detail="Hospital não encontrado")

        deleted = crud.delete_hospital(db, db_hospital)

        log(
            "Tentativa de deletar hospital de ID %s, por parte do usuário %s: %s"
            % (hospital_id, logged_user.name, deleted),
            db,
            user_id=logged_user.id,
        )

        return deleted

    log(
        f"Usuário {logged_user.name}, que não é superuser, tentou deletar hospital",
        db,
        user_id=logged_user.id,
    )
    raise HTTPException(
        status_code=403, detail="Um usuário sem permissão tentou apagar hospital"
    )

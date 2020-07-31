"""
Results router
"""
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from .. import crud, log, schemas
from ..auth import oauth2_scheme
from ..deps import get_db


router = APIRouter()

# pylint: disable=too-many-arguments
@router.get("/results/", response_model=List[schemas.Result])
def read_results(
    db: Session = Depends(get_db),
    dnv: str = "",
    cns: str = "",
    cpf: str = "",
    data_nasc: str = "",
    data_coleta: str = "",
    local_coleta: str = "",
    mother_firstname: str = "",
    mother_surname: str = "",
    token: str = Depends(oauth2_scheme),
):
    """
    Lista resultados conforme os filtros: resultados cujo DNV é dado
    e o CNS também é dado e assim por diante.

    Se deixar o filtro vazio, ele não será considerado.
    Por exemplo, deixar todos os filtros vazios faz com que
    sejam listados todos os resultados existentes no banco.

    Filtros de nome da mãe e de local de coleta funcionam com operador LIKE:
        Colocar Ana fará com que apenas mães com nome = Ana apareçam.
        Colocar Ana% fará com que mães com nome que começa com Ana apareçam.
        Colocar %Ana% fará com que mães com nome que contém Ana apareçam.

    O mesmo vale pros locais de coleta.
    """

    logged_user = crud.get_current_user(db, token)
    if not (logged_user.is_superuser or logged_user.is_staff):
        cpf = logged_user.cpf

    result_list = crud.read_results(
        db,
        dnv,
        cns,
        cpf,
        data_nasc,
        data_coleta,
        local_coleta,
        mother_firstname,
        mother_surname,
    )

    log(
        "Resultados foram buscados com os seguintes filtros: DNV = %s, "
        "CNS = %s, CPF = %s, DataNasc = %s, DataColeta = %s, "
        "LocalColeta = %s, prMotherFirstname = %s, prMotherSurname = %s, pelo usuário %s"
        % (
            dnv,
            cns,
            cpf,
            data_nasc,
            data_coleta,
            local_coleta,
            mother_firstname,
            mother_surname,
            logged_user.name,
        ),
        db,
        user_id=logged_user.id,
    )

    return result_list


@router.post(
    "/result_creation_just_for_test/", response_model=schemas.Result, status_code=201
)
def create_result_just_for_test(
    result: schemas.ResultCreate, db: Session = Depends(get_db)
):
    """
    Receives a new result record in `result` and creates
    a new result in the current database
    """
    created_result = crud.create_result(db=db, result=result)

    log(
        f"[CRIAÇÃO DE RESULTADO] Foi criado um resultado para fins de teste. ID do resultado de teste: {created_result.id}",
        db,
        results_id=created_result.id,
    )

    return created_result

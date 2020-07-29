"""
CRUD = Create Read Update Delete
"""

from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from api_pezao.models.log import Log
from api_pezao.models.user import User


from .. import models, schemas
from ..auth import get_password_hash

from .hospital import *
from .user import *

# pylint: disable=too-many-arguments
def read_results(
    db: Session,
    dnv: str = "",
    cns: str = "",
    cpf: str = "",
    data_nascimento: str = "",
    data_coleta: str = "",
    local_coleta: str = "",
    mother_firstname: str = "",
    mother_surname: str = "",
):
    """
    Lista resultados conforme os filtros: resultados cujo DNV é dado e o CNS também,
    é dado e assim por diante.

    Se deixar o filtro vazio, ele não será considerado.
    Por exemplo, deixar todos os filtros vazios faz com que sejam listados todos
    os resultados existentes no banco.

    Filtros de nome da mãe e de local de coleta funcionam com operador LIKE:
        Colocar Ana fará com que apenas mães com nome = Ana apareçam.
        Colocar Ana% fará com que mães com nome que começa com Ana apareçam.
        Colocar %Ana% fará com que mães com nome que contém Ana apareçam.

    O mesmo vale pros locais de coleta.
    """
    results = db.query(models.Result)

    if dnv != "":
        results = results.filter(models.Result.DNV == dnv)
    if cns != "":
        results = results.filter(models.Result.CNS == cns)
    if cpf != "":
        results = results.filter(models.Result.CPF == cpf)
    if data_nascimento != "":
        results = results.filter(models.Result.DataNasc == data_nascimento)
    if data_coleta != "":
        results = results.filter(models.Result.DataColeta == data_coleta)
    if local_coleta != "":
        results = results.filter(models.Result.LocalColeta.like(local_coleta))
    if mother_firstname != "":
        results = results.filter(models.Result.prMotherFirstname.like(mother_firstname))
    if mother_surname != "":
        results = results.filter(models.Result.prMotherSurname.like(mother_surname))

    results = results.order_by(models.Result.FILE_EXPORT_DATE.desc())

    return results.all()


def test_get_hospital_user(db: Session, hospital_id: int):
    """
    Função de teste
    """
    db_hospital = (
        db.query(models.HospitalCS).filter(models.HospitalCS.id == hospital_id).first()
    )
    return db_hospital.user


def list_logs(db: Session) -> List[Log]:
    """
    Lists all the registered users
    """
    return db.query(models.Log).all()

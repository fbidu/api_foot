"""
CRUD = Create Read Update Delete
"""
import re

from sqlalchemy.orm import Session

from .. import models, schemas


# pylint: disable=too-many-arguments, invalid-name
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
    PDF_Filename: str = "",
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
        dnv = "".join(re.findall(r"\d", dnv))
        results = results.filter(models.Result.DNV == dnv)
    if cns != "":
        cns = "".join(re.findall(r"\d", cns))
        results = results.filter(models.Result.CNS == cns)
    if cpf != "":
        cpf = "".join(re.findall(r"\d", cpf))
        results = results.filter(models.Result.CPF == cpf)
    if data_nascimento != "":
        results = results.filter(models.Result.DataNasc == data_nascimento)
    if data_coleta != "":
        results = results.filter(models.Result.DataColeta == data_coleta)
    if local_coleta != "":
        results = results.filter(
            models.Result.LocalColeta.ilike("%" + local_coleta + "%")
        )
    if mother_firstname != "":
        results = results.filter(
            models.Result.prMotherFirstname.ilike("%" + mother_firstname + "%")
        )
    if mother_surname != "":
        results = results.filter(
            models.Result.prMotherSurname.ilike("%" + mother_surname + "%")
        )
    if PDF_Filename != "":
        results = results.filter(models.Result.PDF_Filename.like(PDF_Filename))

    results = results.order_by(models.Result.FILE_EXPORT_DATE.desc())

    return results.all()


def create_result(db: Session, result: schemas.ResultCreate):
    """
    Creates a new result from the data in the schema inside the provided DB
    """
    db_result = models.Result(**result.dict())

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result

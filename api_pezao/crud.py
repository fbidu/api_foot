"""
CRUD = Create Read Update Delete
"""

from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user from the data in the schema inside the provided DB
    """
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def list_users(db: Session):
    """
    Lists all the registered users
    """
    return db.query(models.User).all()

def create_result(db: Session, result: schemas.ResultCreate):
    """
    Creates a new result from the data in the schema inside the provided DB
    """
    db_result = models.Result(**result.dict())

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result

def read_results(
db: Session, DNV: str = "", CNS: str = "", CPF: str = "", DataNasc: str = "", DataColeta: str = "", LocalColeta: str = "", prMotherFirstname: str = "", prMotherSurname: str = ""
):
    """
    Lista resultados conforme os filtros: resultados cujo DNV é o dado e o CNS também é o dado e assim por diante.
    Se deixar o filtro vazio, ele não será considerado. Por exemplo, deixar todos os filtros vazios faz com que sejam listados todos os resultados existentes no banco.
    Filtros de nome da mãe e de local de coleta funcionam com operador LIKE.
    Colocar Ana fará com que apenas mães com nome = Ana apareçam.
    Colocar Ana% fará com que mães com nome que começa com Ana apareçam.
    Colocar %Ana% fará com que mães com nome que contém Ana apareçam.
    O mesmo vale pros locais de coleta.
    """
    results = db.query(models.Result)

    if not DNV == "":
        results = results.filter(models.Result.DNV == DNV)
    if not CNS == "":
        results = results.filter(models.Result.CNS == CNS)
    if not CPF == "":
        results = results.filter(models.Result.CPF == CPF)
    if not DataNasc == "":
        results = results.filter(models.Result.DataNasc == DataNasc)
    if not DataColeta == "":
        results = results.filter(models.Result.DataColeta == DataColeta)
    if not LocalColeta == "":
        results = results.filter(models.Result.LocalColeta.like(LocalColeta))
    if not prMotherFirstname == "":
        results = results.filter(models.Result.prMotherFirstname.like(prMotherFirstname))
    if not prMotherSurname == "":
        results = results.filter(models.Result.prMotherSurname.like(prMotherSurname))

    results = results.order_by(models.Result.FILE_EXPORT_DATE.desc())

    return results.all()

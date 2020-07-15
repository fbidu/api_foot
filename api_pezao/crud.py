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

def list_results(db: Session):
    """
    Lists all the registered results
    """
    return db.query(models.Result).all()

def get_results_by_dnv(db: Session, dnv: str):
    """
    Lista todos os resultados cujo DNV é o DNV dado.
    """
    return db.query(models.Result).filter(models.Result.DNV == dnv).all()

def get_results_by_cns(db: Session, cns: str):
    """
    Lista todos os resultados cujo CNS é o CNS dado.
    """
    return db.query(models.Result).filter(models.Result.CNS == cns).all()


def get_results_by_cpf(db: Session, cpf: str):
    """
    Lista todos os resultados cujo CPF é o CPF dado.
    """
    return db.query(models.Result).filter(models.Result.CPF == cpf).all()

def get_results_by_datanasc(db: Session, datanasc: str):
    """
    Lista todos os resultados cuja data de nascimento é a data dada.
    """
    return db.query(models.Result).filter(models.Result.DataNasc == datanasc).all()

def get_results_by_datacoleta(db: Session, datacoleta: str):
    """
    Lista todos os resultados cuja data de nascimento é a data dada.
    """
    return db.query(models.Result).filter(models.Result.DataColeta == datacoleta).all()

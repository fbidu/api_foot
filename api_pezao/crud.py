"""
CRUD = Create Read Update Delete
"""
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from api_pezao.models.user import User


from . import models, schemas
from .auth import get_password_hash


def create_user(db: Session, user: schemas.UserCreate) -> User:
    """
    Creates a new user from the data in the schema inside the provided DB
    """
    db_user = models.User(**user.dict())
    db_user.password = get_password_hash(db_user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def list_users(db: Session) -> List[User]:
    """
    Lists all the registered users
    """
    return db.query(models.User).all()

def find_user(db: Session, email: str = None, cpf: str = None) -> User:
    """
    Procura por um usuário por email ou cpf.

    Se os dois campos - email e cpf - forem fornecidos,
    essa função vai buscar por usuário que tenha tanto o
    e-mail quanto o CPF igual ao da função.

    Se nenhum dos campos for fornecido, a função retorna None

    Args:
        db (sqlalchemy.orm.Session): Sessão do SQLAlchemy para buscar o usuário
        email (str, opcional): e-mail para ser buscado
        cpf (str, opcional): CPF para ser buscado
    """

    if not (email or cpf):
        return None

    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)
    if cpf:
        query = query.filter(models.User.cpf == cpf)

    return query.first()


def get_current_user(db: Session, token: str):
    """
    Retorna informações do usuário logado
    """
    user = find_user(db, email=token)
    return user

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

def read_hospitals(db: Session, code: str = "", name: str = "", email: str = ""):
    hospitals = db.query(models.HospitalCS)

    if not code == '':
        hospitals = hospitals.filter(models.HospitalCS.code == code)
    if not name == '':
        hospitals = hospitals.filter(models.HospitalCS.name.like(name))
    if not email == '':
        hospitals = hospitals.filter(
            or_(
                models.HospitalCS.email1.like(email),
                models.HospitalCS.email2.like(email),
                models.HospitalCS.email3.like(email),
            )
        )

    return hospitals.all()

def create_hospital(db: Session, hospital: schemas.HospitalCSCreate, password: str):
    """
    Creates a new hospital from the data in the schema inside the provided DB
    """
    db_hospital = models.HospitalCS(**hospital.dict())

    hospital_user = schemas.UserCreate(cpf="", email=db_hospital.email1, password=password)
    created_user = create_user(db, hospital_user)

    db_hospital.user_id = created_user.id

    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)

    return db_hospital

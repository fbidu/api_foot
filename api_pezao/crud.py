"""
CRUD = Create Read Update Delete
"""

from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from api_pezao.models.log import Log
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


def set_staff_role(user: schemas.User, staff: bool, db: Session) -> User:
    """
    Muda um usuário para staff
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_staff = staff
        db.commit()
        db.refresh(db_user)

    return db_user


def set_superuser_role(user: schemas.User, superuser: bool, db: Session) -> User:
    """
    Muda um usuário para super_user
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_superuser = superuser
        db.commit()
        db.refresh(db_user)

    return db_user


def list_users(db: Session) -> List[User]:
    """
    Lists all the registered users
    """
    return db.query(models.User).all()


def find_user(db: Session, username: str) -> User:
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

    query = db.query(models.User)
    user = query.filter(models.User.cpf == username).first()

    if user is None:
        user = query.filter(models.User.email == username).first()
    if user is None:
        user = query.filter(models.User.login == username).first()

    return user


def get_current_user(db: Session, token: str):
    """
    Retorna informações do usuário logado
    """
    user = find_user(db, username=token)
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


def read_hospitals(db: Session, code: str = "", name: str = "", email: str = ""):
    """
    Lista hospitais na base
    """
    hospitals = db.query(models.HospitalCS)

    if code != "":
        hospitals = hospitals.filter(models.HospitalCS.code == code)
    if name != "":
        hospitals = hospitals.filter(models.HospitalCS.name.like(name))
    if email != "":
        hospitals = hospitals.filter(
            or_(
                models.HospitalCS.email1.like(email),
                models.HospitalCS.email2.like(email),
                models.HospitalCS.email3.like(email),
            )
        )

    return hospitals.all()


def create_hospital(db: Session, hospital: schemas.HospitalCSCreate):
    """
    Cria um novo hospital
    """
    db_hospital = models.HospitalCS(**hospital.dict(exclude={"password"}))

    user = schemas.UserCreate(
        cpf=None,
        email=None,
        name=hospital.name,
        login=hospital.code + "-" + hospital.type,
        password=hospital.password,
    )

    db_user = create_user(db, user)
    db_user.is_staff = True

    db_hospital.user_id = db_user.id

    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)

    return db_hospital


def update_hospital(db: Session, hospital: schemas.HospitalCSUpdate):
    """
    Atualiza um hospital
    """
    db_hospital = (
        db.query(models.HospitalCS).filter(models.HospitalCS.id == hospital.id).first()
    )

    if db_hospital:
        db_hospital.code = hospital.code
        db_hospital.name = hospital.name
        db_hospital.type = hospital.type
        db_hospital.email1 = hospital.email1
        db_hospital.email2 = hospital.email2
        db_hospital.email3 = hospital.email3
        db_hospital.updated_at = datetime.now()

        db_user = db_hospital.user

        if db_user:
            db_user.name = hospital.name
            db_user.login = hospital.code + "-" + hospital.type
            db_user.updated_at = datetime.now()

            if hospital.password:
                db_user.password = get_password_hash(hospital.password)

            db.commit()
            db.refresh(db_user)

        db.commit()
        db.refresh(db_hospital)

        return db_hospital
    return None


def delete_hospital(db: Session, hospital_id: int):
    """
    Deleta um hospital
    """
    db_hospital = (
        db.query(models.HospitalCS).filter(models.HospitalCS.id == hospital_id).first()
    )

    if db_hospital is None:
        return False

    db_user = db_hospital.user

    db.delete(db_hospital)

    if db_user:
        db.delete(db_user)

    db.commit()

    return True


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

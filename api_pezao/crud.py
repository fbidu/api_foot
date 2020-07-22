"""
CRUD = Create Read Update Delete
"""

from typing import List
from typing import Tuple

from sqlalchemy.orm import Session
from sqlalchemy import or_

from api_pezao.models.log import Log
from api_pezao.models.user import User


from . import models, schemas,sms_utils
from .auth import get_password_hash

from datetime import datetime


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


def find_user(db: Session, login_possibility: str = None) -> User:
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

    if not login_possibility:
        return None

    query = db.query(models.User)
    user = query.filter(models.User.cpf == login_possibility).first()

    if user is None:
        user = query.filter(models.User.email == login_possibility).first()

    if user is None:
        user = query.filter(models.User.login == login_possibility).first()

    return user


def get_current_user(db: Session, token: str):
    """
    Retorna informações do usuário logado
    """
    user = find_user(db, login_possibility=token)
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
    db_hospital = models.HospitalCS(**hospital.dict())

    user = schemas.UserCreate(cpf=None, email=None, name=hospital.name,
                            login=hospital.code+"-"+hospital.type, password=password)

    db_user = create_user(db, user)

    db_hospital.user_id = db_user.id

    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)

    return db_hospital


def update_hospital(db: Session, hospital: schemas.HospitalCS, password: str = None):
    db_hospital = db.query(models.HospitalCS).filter(models.HospitalCS.id == hospital.id).first()

    if not db_hospital == None:
        db_hospital.code = hospital.code
        db_hospital.name = hospital.name
        db_hospital.type = hospital.type
        db_hospital.email1 = hospital.email1
        db_hospital.email2 = hospital.email2
        db_hospital.email3 = hospital.email3
        db_hospital.updated_at = datetime.now()

        db_user = db_hospital.user

        if not db_user == None:
            db_user.name = hospital.name
            db_user.login = hospital.code+"-"+hospital.type
            db_user.updated_at = datetime.now()

            if not password == None:
                db_user.password = get_password_hash(password)

            db.commit()
            db.refresh(db_user)

        db.commit()
        db.refresh(db_hospital)

        return db_hospital


def delete_hospital(db: Session, hospital_id: int):
    db_hospital = db.query(models.HospitalCS).filter(models.HospitalCS.id == hospital_id).first()

    if db_hospital == None:
        return False

    db_user = db_hospital.user

    db.delete(db_hospital)

    if db_user is not None:
        db.delete(db_user)

    db.commit()

    return True


def test_get_hospital_user(db: Session, hospital_id: int):
    db_hospital = db.query(models.HospitalCS).filter(models.HospitalCS.id == hospital_id).first()
    return db_hospital.user


def list_logs(db: Session) -> List[Log]:
    """
    Lists all the registered users
    """
    return db.query(models.Log).all()


def sms_sweep(db: Session, hospital_list: List[str] = None):
    """
    Returns a (phone, message, result id) for every SMS that needs to be sent
    If a list of hospitals is provided, returns SMSs to be sent from exams made in those hospitals only
    """

    if not hospital_list:
        # no defined hospitals -> return every result which SMS hadn't been sent yet
        result_list = db.query(models.Result).filter(not models.Result.sms_sent).all()
    else:
        # defined hospitals -> return not sent results whose hospital code is in hospitals list
        result_list = db.query(models.Result).filter(not models.Result.sms_sent,
                                                     models.Result.COD_LocColeta.in_(hospital_list)).all()

    # creates a list of SMS to be returned
    # every entry in the list is a tuple (phone, message)
    sms_list = []

    # for each result that needs SMS to be sent:
    for r in result_list:

        valid_phones = []
        error_codes = []

        # checks if there are valid mobile phone numbers for sending SMS on that result.
        # valid numbers are saved to the valid_phones list
        # error codes (0: no phones, 1: no mobile phones, 2: invalid ddd) are saved on error_codes list
        for phone in [r.ptnPhone1, r.ptnPhone2]:
            if phone:
                v = sms_utils.verify_phone(v)
                if isinstance(v, int):
                    error_codes.append(v)
                else:
                    valid_phones.append(v)

        # if there are no valid numbers, report back the gravest error found (smaller number)
        if not valid_phones:
            error_codes.sort()
            sms_list.append((str(error_codes[0]), None, r.id))

        else:
            # if there are valid phones...

            # find the sms message to be sent:
            # look in the template_results table for the entry with same result_id as the result's id
            # then, look in the template_sms table for the entry with same id as the discovered
            # template_results' template_id
            for message in r.templates_result:
                for p in valid_phones:
                    sms_list. append((p, message.templates_sms.msg, r.id))

    # returns list of sms messages to be sent
    return sms_list


def confirm_sms(db: Session, result_id):
    db_result = db.query(models.Result).filter(models.Result.id == result_id)
    db_result.sms_sent = True

    db.commit()
    db.refresh(db_result)
    return True

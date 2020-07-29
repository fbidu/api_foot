"""
CRUD para hospitais
"""
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas
from ..auth import get_password_hash

from .user import create_user


def read_hospitals(
    db: Session, id_: int = None, code: str = "", name: str = "", email: str = ""
):
    """
    Lista hospitais na base
    """
    hospitals = db.query(models.HospitalCS)

    if id_ is not None:
        hospitals = hospitals.filter(models.HospitalCS.id == id_)
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


def update_hospital(
    db: Session, db_hospital: models.HospitalCS, hospital: schemas.HospitalCSUpdate
):
    """
    Atualiza um hospital
    """

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

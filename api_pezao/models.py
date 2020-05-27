"""
Armazenar os modelos de dados para o banco
"""
import enum
import datetime
from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


# pylint: disable=too-few-public-methods
class HospitalType(enum.Enum):
    H = 'H'
    C = 'C'

class User(Base):
    """
    Defines the SQLAlchemy model for 'user' table
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class RolesUsers(Base):
    """
    Defines the SQLAlchemy model for 'roles_users' table
    """

    __tablename__ = "roles_users"

    user_id = Column(Integer, unique=True, index=True)
    role_id = Column(Integer, unique=True, index=True)

class Roles(Base):
    """
    Defines the SQLAlchemy model for 'roles' table
    """

    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)

class Hospital_Cs(Base):
    """
    Defines the SQLAlchemy model for 'hospital_cs' table
    """

    __tablename__ = "hospital_cs"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(enum.Enum(HospitalType))
    email1 = Column(String)
    email2 = Column(String)
    email3 = Column(String)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Log(Base):
    """
    Defines the SQLAlchemy model for 'log' table
    """

    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    results_id = Column(Integer, unique=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    client_ip = Column(String)
    client_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Templates_Result(Base):
    """
    Defines the SQLAlchemy model for 'templates_result' table
    """

    __tablename__ = "templates_result"

    result_id = Column(Integer, unique=True, index=True)
    template_id = Column(Integer, unique=True, index=True)

class Templates_SMS(Base):
    """
    Defines the SQLAlchemy model for 'templates_sms' table
    """

    __tablename__ = "templates_sms"

    id = Column(Integer, primary_key=True, index=True)
    msg = Column(String)

class Attempt_Log(Base):
    """
    Defines the SQLAlchemy model for 'attempt_log' table
    """

    __tablename__ = "attempt_log"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)
    correct_code = Column(String)
    code = Column(String)
    cpf = Column(String)
    dnv = Column(String)
    dtnasc = Column(String)
    client_ip = Column(String)
    client_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Result(Base):
    """
    Defines the SQLAlchemy model for 'result' table
    """

    #some stuff here im unsure about, waiting for answers from the client, ana will ask her

    __tablename__ = "result"

    id = Column(Integer, primary_key=True, index=True)
    IDExport = Column(Integer, unique=True, index=True)
    Barcode = Column(Integer) #type?
    NumLote = Column(Integer)
    DataNasc = Column(String) #date?
    HoraNasc = Column(String) #date?
    DataColeta = Column(String) #date?
    HoraColeta = Column(String) #date?
    prMotherFirstname = Column(String)
    prMotherSurname = Column(String)
    CPF = Column(String)
    ptnFirstname = Column(String)
    ptnSurname = Column(String)
    DNV = Column(String)
    CNS = Column(String) #type?
    ptnEmail = Column(String)
    ptnPhone1 = Column(String)
    ptnPhone2 = Column(String)
    CodLocColeta = Column(String) #type?
    LocalColeta = Column(String)
    COD_LocColeta = Column(String) #type? repeat?
    COD_HospNasc = Column(String) #type? repeat?
    HospNasc = Column(String)
    LocalNasc = Column(String)
    PDF_Filename = Column(String)
    Tipo_SMS = Column(String) #type?
    RECODRD_CREATION_DATE = Column(DateTime, default=datetime.datetime.utcnow) #date?
    FILE_EXPORT_DATE = Column(DateTime, default=datetime.datetime.utcnow) #date?
    FILE_EXPORT_NAME = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


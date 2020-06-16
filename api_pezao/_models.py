"""
Armazenar os modelos de dados para o banco
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class AttemptLog(Base):
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

    # some stuff here im unsure about, waiting for answers from the client, ana will ask her

    __tablename__ = "result"

    id = Column(Integer, primary_key=True, index=True)
    IDExport = Column(Integer, unique=True, index=True)
    Barcode = Column(String)
    NumLote = Column(Integer)
    DataNasc = Column(String)  # date?
    HoraNasc = Column(String)  # date?
    DataColeta = Column(String)  # date?
    HoraColeta = Column(String)  # date?
    prMotherFirstname = Column(String)
    prMotherSurname = Column(String)
    CPF = Column(String)
    ptnFirstname = Column(String)
    ptnSurname = Column(String)
    DNV = Column(String)
    CNS = Column(String)  # type?
    ptnEmail = Column(String)
    ptnPhone1 = Column(String)
    ptnPhone2 = Column(String)
    CodLocColeta = Column(String)  # type?
    LocalColeta = Column(String)
    COD_LocColeta = Column(String)  # type? repeat?
    COD_HospNasc = Column(String)  # type? repeat?
    HospNasc = Column(String)
    LocalNasc = Column(String)
    PDF_Filename = Column(String)
    Tipo_SMS = Column(String)  # type?
    RECORD_CREATION_DATE = Column(DateTime, default=datetime.datetime.utcnow)  # date?
    FILE_EXPORT_DATE = Column(DateTime, default=datetime.datetime.utcnow)  # date?
    FILE_EXPORT_NAME = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

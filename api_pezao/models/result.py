"""
Define modelo SQL para resultados
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


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
    RECORD_CREATION_DATE = Column(DateTime, default=datetime.utcnow)  # date?
    FILE_EXPORT_DATE = Column(DateTime, default=datetime.utcnow)  # date?
    FILE_EXPORT_NAME = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    sms_sent = Column(Boolean)

    log = relationship("Log", back_populates="result")
    templates_result = relationship("TemplatesResult", back_populates="result")

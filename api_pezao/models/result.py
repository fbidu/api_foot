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
    LotNumber = Column(Integer)
    DataNasc = Column(String)
    HoraNasc = Column(String)
    DataColeta = Column(String)
    prMotherFirstname = Column(String)
    prMotherSurname = Column(String)
    CPF = Column(String)
    ptnFirstname = Column(String)
    ptnSurname = Column(String)
    DNV = Column(String)
    CNS = Column(String)
    ptnEmail = Column(String)
    ptnPhone1 = Column(String)
    ptnPhone2 = Column(String)
    COD_LocColeta = Column(String)
    LocalColeta = Column(String)
    COD_HospitalNasc = Column(String)
    HospitalNasc = Column(String)
    LocalNasc = Column(String)
    PDF_Filename = Column(String)
    PDF_ImageDate = Column(DateTime, default=datetime.utcnow)
    FILE_EXPORT_DATE = Column(DateTime, default=datetime.utcnow)
    FILE_EXPORT_NAME = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    sms_sent = Column(Boolean, default=False)

    log = relationship("Log", back_populates="result")
    templates_result = relationship("TemplatesResult", back_populates="result")

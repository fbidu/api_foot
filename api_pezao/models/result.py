"""
Define modelo SQL para resultados
"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
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
    Barcode = Column(String, nullable=True)
    LotNumber = Column(Integer, nullable=True)
    DataNasc = Column(String, nullable=True)
    HoraNasc = Column(String, nullable=True)
    DataColeta = Column(String, nullable=True)
    prMotherFirstname = Column(String, nullable=True)
    prMotherSurname = Column(String, nullable=True)
    CPF = Column(String, index=True)
    ptnFirstname = Column(String, nullable=True)
    ptnSurname = Column(String, nullable=True)
    DNV = Column(String, index=True)
    CNS = Column(String, index=True)
    ptnEmail = Column(String, nullable=True)
    ptnPhone1 = Column(String, nullable=True)
    ptnPhone2 = Column(String, nullable=True)
    COD_LocColeta = Column(String, nullable=True)
    LocalColeta = Column(String, nullable=True)
    COD_HospitalNasc = Column(String, nullable=True)
    HospitalNasc = Column(String, nullable=True)
    LocalNasc = Column(String, nullable=True)
    PDF_Filename = Column(String, nullable=True)
    PDF_ImageDate = Column(DateTime, default=datetime.utcnow)
    FILE_EXPORT_DATE = Column(DateTime, default=datetime.utcnow)
    FILE_EXPORT_NAME = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    sms_sent = Column(Boolean, default=False)

    log = relationship("Log", back_populates="result")
    templates_result = relationship("TemplatesResult", back_populates="result")

"""
Define modelo de dados para resultados
"""
from datetime import datetime
from pydantic import BaseModel


class ResultBase(BaseModel):
    """
    ResultBase lista os campos que estão sempre disponíveis
    """

    id: int
    IDExport: int
    Barcode: int  # type?
    NumLote: int  # fieldname?
    DataNasc: str  # date?
    HoraNasc: str  # date?
    DataColeta: str  # date?
    HoraColeta: str  # date?
    prMotherFirstname: str  # fieldname?
    prMotherSurname: str  # fieldname?
    CPF: str
    ptnFirstname: str
    ptnSurname: str
    DNV: str
    CNS: str  # type?
    ptnEmail: str
    ptnPhone1: str
    ptnPhone2: str
    CodLocColeta: str  # type?
    LocalColeta: str
    COD_LocColeta: str  # type? repeat? fieldname?
    COD_HospNasc: str  # type? repeat? fieldname?
    HospNasc: str
    LocalNasc: str
    PDF_Filename: str
    Tipo_SMS: str  # type?
    RECORD_CREATION_DATE: datetime  # date?
    FILE_EXPORT_DATE: datetime  # date?
    FILE_EXPORT_NAME: str


class ResultCreate(ResultBase):
    """
    Os campos necessários para criar um novo resultado.
    São os mesmos da base.
    """

    pass


class Result(ResultBase):
    """
    Define um modelo de dados para os resultados
    """

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

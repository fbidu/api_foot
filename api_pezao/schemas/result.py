"""
Define modelo de dados para resultados
"""
from datetime import datetime
from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module
import re

class ResultBase(BaseModel):
    """
    ResultBase lista os campos que estão sempre disponíveis
    """

    IDExport: int
    Barcode: int
    NumLote: int
    DataNasc: str
    HoraNasc: str
    DataColeta: str
    HoraColeta: str
    prMotherFirstname: str
    prMotherSurname: str
    CPF: str
    ptnFirstname: str
    ptnSurname: str
    DNV: str
    CNS: str
    ptnEmail: str
    ptnPhone1: str
    ptnPhone2: str
    CodLocColeta: str
    LocalColeta: str
    COD_LocColeta: str
    COD_HospNasc: str
    HospNasc: str
    LocalNasc: str
    PDF_Filename: str
    Tipo_SMS: str
    RECORD_CREATION_DATE: datetime
    FILE_EXPORT_DATE: datetime
    FILE_EXPORT_NAME: str
    sms_sent: bool = False

    @validator('CPF')
    def cpf_numbers(cls, v):
        return ''.join(re.findall(r"\d", v))

    @validator('CNS')
    def cns_numbers(cls, v):
        return ''.join(re.findall(r"\d", v))

    @validator('DNV')
    def dnv_numbers(cls, v):
        return ''.join(re.findall(r"\d", v))


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

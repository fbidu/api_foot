"""
Define modelo de dados para resultados
"""
import re
from datetime import datetime

from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module


class ResultBase(BaseModel):
    """
    ResultBase lista os campos que estão sempre disponíveis
    """

    IDExport: int
    Barcode: str = None
    LotNumber: str = None
    DataNasc: str = None
    HoraNasc: str = None
    DataColeta: str = None
    prMotherFirstname: str = None
    prMotherSurname: str = None
    CPF: str
    ptnFirstname: str = None
    ptnSurname: str = None
    DNV: str
    CNS: str = None
    ptnEmail: str = None
    ptnPhone1: str = None
    ptnPhone2: str = None
    COD_LocColeta: str = None
    LocalColeta: str = None
    COD_HospitalNasc: str = None
    HospitalNasc: str = None
    LocalNasc: str = None
    PDF_Filename: str = None
    PDF_ImageDate: datetime = None
    FILE_EXPORT_DATE: datetime = None
    FILE_EXPORT_NAME: str = None
    sms_sent: bool = False

    # pylint: disable=invalid-name,missing-function-docstring,no-self-argument,no-self-use
    @validator("CPF")
    def cpf_numbers(cls, v):
        return "".join(re.findall(r"\d", v))

    @validator("CNS")
    def cns_numbers(cls, v):
        return "".join(re.findall(r"\d", v))

    @validator("DNV")
    def dnv_numbers(cls, v):
        return "".join(re.findall(r"\d", v))


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

    # pylint: disable=invalid-name,missing-function-docstring,no-self-argument,no-self-use
    @validator("PDF_Filename")
    def pdf_file(cls, v):
        return f"/pdf/{v}"

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

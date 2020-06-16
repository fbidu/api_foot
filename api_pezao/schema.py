"""
Define Pydantic models for the data structures.
"""

import datetime
from pydantic import BaseModel

# -------------------------------------------------
class AttemptLogBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    id: int
    login: str
    password: str
    correct_code: str
    code: str
    cpf: str
    dnv: str
    dtnasc: str
    client_ip: str


class AttemptLogCreate(AttemptLogBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class AttemptLog(AttemptLogBase):
    """
    Defines a Pydantic model for an user
    """

    id: int
    client_date_time: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class ResultBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    id: int
    IDExport: int
    Barcode: int  # type?
    NumLote: int  # fieldname?
    DataNasc: str  # date?
    HoraNasc: str  # date?
    DataColeta: str  # date?
    HoraColeta: str  # date?
    ptnMotherFirstname: str  # fieldname?
    ptnMotherSurname: str  # fieldname?
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
    RECODRD_CREATION_DATE: datetime.datetime  # date?
    FILE_EXPORT_DATE: datetime.datetime  # date?
    FILE_EXPORT_NAME: str


class ResultCreate(ResultBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Result(ResultBase):
    """
    Defines a Pydantic model for an user
    """

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

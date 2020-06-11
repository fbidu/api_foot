"""
Define Pydantic models for the data structures.
"""

import datetime
from pydantic import BaseModel

# pylint: disable=too-few-public-methods

# a little confused on this whole part, did i do the bases right?
class UserBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    id: int
    cpf: str
    email: str
    password: str
    created_at: datetime = None  # datetime?
    updated_at: datetime = None  # datetime?


class UserCreate(UserBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class User(UserBase):  # i dont understand this bit :(
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -----------------------------------------------


class Roles_UsersBase(BaseModel):
    """
    Roles_UsersBase defines the fields available for an role_user in any
    point of its lifecycle.
    """

    # descriptions are a bit wonky, im a little lost

    user_id: int
    role_id: int


class Roles_UsersCreate(Roles_UsersBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Roles_Users(Roles_UsersBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class RolesBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    role_id: int
    role_name: str


class RolesCreate(RolesBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Roles(RolesBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class Hospital_CsBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    id: int
    code: str
    name: str
    type: enumerate
    email1: str
    email2: str
    email3: str
    user_id: int
    created_at: datetime  # datetime?
    updated_at: datetime  # datetime?


class Hospital_CsCreate(Hospital_CsBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Hospital_Cs(Hospital_CsBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class LogBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    id: int
    results_id: int
    user_id: int
    client_ip: str
    client_date_time: datetime  # datetime?
    created_at: datetime  # datetime?
    updated_at: datetime  # datetime?


class LogCreate(LogBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Log(LogBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class Templates_ResultBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    result_id: int
    template_id: int


class Templates_ResultCreate(Templates_ResultBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Templates_Result(Templates_ResultBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class Templates_SMSBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    id: int
    msg: str


class Templates_SMSCreate(Templates_SMSBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Templates_SMS(Templates_SMSBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


# -------------------------------------------------
class Attempt_LogBase(BaseModel):
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
    client_date_time: datetime  # datetime?
    created_at: datetime  # datetime?
    updated_at: datetime  # datetime?


class Attempt_LogCreate(Attempt_LogBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class Attempt_Log(Attempt_LogBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

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
    RECODRD_CREATION_DATE: datetime  # date?
    FILE_EXPORT_DATE: datetime  # date?
    FILE_EXPORT_NAME: str
    created_at: datetime  # datetime?
    updated_at: datetime  # datetime?


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

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

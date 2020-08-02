"""
Modelos para log de tentativa de login
"""
from datetime import datetime

from pydantic import BaseModel


class AttemptLogBase(BaseModel):
    """
    Campos que sempre estão presentes numa tentativa de login
    """

    login: str
    password: str
    correct_code: str
    code: str
    cpf: str
    dnv: str
    dtnasc: str
    client_ip: str
    client_date_time: datetime


class AttemptLogCreate(AttemptLogBase):
    """
    Campos necessários para cadastrar um log de tentativa de
    login. São os mesmos de `AttemptLogBase`
    """

    pass


class AttemptLog(AttemptLogBase):
    """
    Campos presentes num log de tentativa de login.
    """

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

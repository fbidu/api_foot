"""
Modelos de validação para Hospitais e Centros de Saúde
"""
from datetime import datetime

from pydantic import BaseModel


class HospitalCSBase(BaseModel):
    """
    Hospital Centro de Saúde Base define campos que sempre estão
    presentes no fluxo dos dados
    """

    code: str
    name: str
    type: str
    email1: str
    email2: str
    email3: str


class HospitalCSCreate(HospitalCSBase):
    """
    Define o comportamento de criação de uma instância de HospitalCS
    """

    password: str


class HospitalCS(HospitalCSBase):
    """
    Modelo de validação para um Hospital Centro de Saúde
    """

    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    deleted: bool = False

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True


class HospitalCSUpdate(HospitalCSBase):
    """
    Modelo para atualização de hospital.
    """

    password: str = None

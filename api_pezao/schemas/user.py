"""
Oferece modelos de validação para Usuários
"""
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    cpf: str
    email: str
    password: str


class UserCreate(UserBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class User(UserBase):
    """
    Defines a Pydantic model for an user
    """

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

"""
Oferece modelos de validação para Usuários
"""
from datetime import datetime
from pydantic import BaseModel, root_validator  # pylint: disable=no-name-in-module


class UserBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    cpf: str = None
    name: str
    email: str = None
    login: str = None

    @root_validator
    def check_user_has_at_least_one(cls, values):
        user_cpf = values.get('cpf')
        user_email = values.get('email')
        user_login = values.get('login')
        if user_cpf is None and user_email is None and user_login is None:
            raise ValueError('User should have at least one of these: cpf, email, login')
        return values


class UserCreate(UserBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    password: str


class User(UserBase):
    """
    Defines a Pydantic model for an user
    """

    id: int
    created_at: datetime
    updated_at: datetime
    is_superuser: bool
    is_staff: bool

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

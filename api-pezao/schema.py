"""
Define Pydantic models for the data structures.
"""
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class UserBase(BaseModel):
    """
    UserBase defines the fields available for an user in any
    point of its lifecycle.
    """

    email: str
    cpf: str
    first_name: str = None
    last_name: str = None


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

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

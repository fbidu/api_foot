"""
Modelos de validação para as relações entre Usuário e Roles
"""
from pydantic import BaseModel


class RolesUsersBase(BaseModel):
    """
    Roles_UsersBase defines the fields available for an role_user in any
    point of its lifecycle.
    """

    # descriptions are a bit wonky, im a little lost

    user_id: int
    role_id: int


class RolesUsersCreate(RolesUsersBase):
    """
    UserCreate defines additional fields that should be used
    while creating an user that weren't defined on `UserBase`
    """

    pass


class RolesUsers(RolesUsersBase):
    """
    Defines a Pydantic model for an user
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

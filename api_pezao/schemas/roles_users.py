"""
Modelos de validação para as relações entre Usuário e Roles
"""
from pydantic import BaseModel


class RolesUsersBase(BaseModel):
    """
    RolesUsersBase define a base para relação user-role.
    Essa relação sempre possuirá user_id e role_id
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

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

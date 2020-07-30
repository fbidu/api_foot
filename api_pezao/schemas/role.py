"""
Define validadores para os Roles, que são os papeis
que um usuário pode ter dentro do sistema
"""
from pydantic import BaseModel


class RoleBase(BaseModel):
    """
    Um role sempre vai possuir nome
    """

    role_name: str


class RoleCreate(RoleBase):
    """
    Ao criar um role precisamos apenas do Nome, que já
    está definido como necessário na clase RoleBase
    """

    pass


class Role(RoleBase):
    """
    Um role é um papel que o usuário possui no sistema.

    Atributos:

        * role_id (int): o ID do role
        * role_name (str): o nome do role
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

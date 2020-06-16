"""
Define validações para Templates de SMS
"""

from pydantic import BaseModel


class TemplatesSMSBase(BaseModel):
    """
    A base do modelo é um campo 'msg', que contém o template em si
    """

    msg: str


class TemplatesSMSCreate(TemplatesSMSBase):
    """
    Campos necessários ao criar um novo template. Precisamos
    apenas dos campos da Base
    """

    pass


class TemplatesSMS(TemplatesSMSBase):
    """
    Define um template SMS em si
    """

    id: int

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

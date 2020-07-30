"""
Define validações para a relação entre resultados e templates
"""
from pydantic import BaseModel


class TemplatesResultBase(BaseModel):
    """
    Valida campos que são sempre necessários ao lidar com templates
    """

    result_id: int
    template_id: int


class TemplatesResultCreate(TemplatesResultBase):
    """
    Ao criar uma relação template - resultado, os campos necessários
    são os mesmos da base
    """

    pass


class TemplatesResult(TemplatesResultBase):
    """
    Define a visualização da relação entre template
    e resultado
    """

    pass

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

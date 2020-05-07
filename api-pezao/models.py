"""
Armazenar os modelos de dados para o banco
"""
from sqlalchemy import Column, Integer, String

from .database import Base


# pylint: disable=too-few-public-methods
class User(Base):
    """
    Defines the SQLAlchemy model for an user
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

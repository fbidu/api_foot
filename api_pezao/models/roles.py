"""
Define modelo SQL para Roles
"""
from sqlalchemy import Column, Integer, String

from ..database import Base


class Roles(Base):
    """
    Defines the SQLAlchemy model for 'roles' table
    """

    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)

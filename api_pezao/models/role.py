"""
Define modelo SQL para Roles
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Role(Base):
    """
    Defines the SQLAlchemy model for 'roles' table
    """

    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)

    roles_users = relationship("RolesUsers", back_populates="role")

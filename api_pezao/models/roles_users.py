"""
Define modelo SQL para relação User e Role
"""
from sqlalchemy import Column, Integer, PrimaryKeyConstraint

from ..database import Base


class RolesUsers(Base):
    """
    Defines the SQLAlchemy model for 'roles_users' table
    """

    __tablename__ = "roles_users"
    __table_args__ = (PrimaryKeyConstraint("user_id", "role_id"),)
    user_id = Column(Integer, index=True)
    role_id = Column(Integer, index=True)

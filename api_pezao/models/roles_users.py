"""
Define modelo SQL para relação User e Role
"""
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class RolesUsers(Base):
    """
    Defines the SQLAlchemy model for 'roles_users' table
    """

    __tablename__ = "roles_users"
    __table_args__ = (PrimaryKeyConstraint("user_id", "role_id"),)
    user_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.id'))

    user = relationship("User", back_populates="roles_users")
    role = relationship("Role", back_populates="roles_users")

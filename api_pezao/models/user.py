"""
Define modelo SQL para User
"""
import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    """
    Defines the SQLAlchemy model for 'user' table
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    log = relationship("Log", back_populates="user")
    roles_users = relationship("RolesUsers", back_populates="user")
    hospital_cs = relationship("HospitalCS", uselist=False, back_populates="user")

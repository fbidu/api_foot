"""
Define modelo SQL para Hospital CS
"""
import datetime
import enum

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class HospitalType(enum.Enum):
    """
    Enum for the different Hospital Types
    """

    H = "H"
    C = "C"


class HospitalCS(Base):
    """
    Defines the SQLAlchemy model for 'hospital_cs' table
    """

    __tablename__ = "hospital_cs"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(String)
    email1 = Column(String)
    email2 = Column(String)
    email3 = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="hospital_cs")

"""
Define modelo SQL para logs
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Log(Base):
    """
    Defines the SQLAlchemy model for 'log' table
    """

    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    results_id = Column(Integer, ForeignKey("result.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    client_ip = Column(String, nullable=True)
    message = Column(String)
    client_date_time = Column(DateTime, default=datetime.utcnow, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    result = relationship("Result", back_populates="log")
    user = relationship("User", back_populates="log")

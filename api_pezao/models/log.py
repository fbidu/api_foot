"""
Define modelo SQL para logs
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from ..database import Base


class Log(Base):
    """
    Defines the SQLAlchemy model for 'log' table
    """

    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    results_id = Column(Integer, unique=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    client_ip = Column(String)
    client_date_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

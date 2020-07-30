"""
Define modelo SQL para log de tentativa de login
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from ..database import Base


class AttemptLog(Base):
    """
    Defines the SQLAlchemy model for 'attempt_log' table
    """

    __tablename__ = "attempt_log"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)
    correct_code = Column(String)
    code = Column(String)
    cpf = Column(String)
    dnv = Column(String)
    dtnasc = Column(String)
    client_ip = Column(String)
    client_date_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

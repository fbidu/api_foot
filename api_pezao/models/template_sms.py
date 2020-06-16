"""
Define templates SMS
"""
from sqlalchemy import Column, Integer, String

from ..database import Base


class TemplateSMS(Base):
    """
    Defines the SQLAlchemy model for 'templates_sms' table
    """

    __tablename__ = "templates_sms"

    id = Column(Integer, primary_key=True, index=True)
    msg = Column(String)

"""
Define relação entre Templates e Resultados
"""
from sqlalchemy import Column, Integer, PrimaryKeyConstraint

from ..database import Base


class TemplatesResult(Base):
    """
    Defines the SQLAlchemy model for 'templates_result' table
    """

    __tablename__ = "templates_result"
    __table_args__ = (PrimaryKeyConstraint("result_id", "template_id"),)
    result_id = Column(Integer, index=True)
    template_id = Column(Integer, index=True)

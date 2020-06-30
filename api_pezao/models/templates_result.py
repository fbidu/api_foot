"""
Define relação entre Templates e Resultados
"""
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class TemplatesResult(Base):
    """
    Defines the SQLAlchemy model for 'templates_result' table
    """

    __tablename__ = "templates_result"
    __table_args__ = (PrimaryKeyConstraint("result_id", "template_id"),)
    result_id = Column(Integer, ForeignKey('result.id'))
    template_id = Column(Integer, ForeignKey('templates_sms.id'))

    result = relationship("Result", back_populates="templates_result")
    template_sms = relationship("TemplateSMS", back_populates="templates_result")

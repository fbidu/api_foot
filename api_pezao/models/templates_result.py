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
    __table_args__ = (PrimaryKeyConstraint("IDExport", "template_id"),)
    IDExport = Column(Integer, ForeignKey("result.IDExport"))
    template_id = Column(Integer, ForeignKey("templates_sms.id"))

    result = relationship("Result", back_populates="templates_result")
    template_sms = relationship("TemplateSMS", back_populates="templates_result")

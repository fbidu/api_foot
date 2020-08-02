"""
Define relação entre Templates e Resultados
"""
from sqlalchemy import Column, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from ..database import Base


class TemplatesResult(Base):
    """
    Defines the SQLAlchemy model for 'templates_result' table
    """

    __tablename__ = "templates_result"
    __table_args__ = (PrimaryKeyConstraint("IDExport", "template_id"),)
    IDExport = Column(Integer)
    template_id = Column(Integer)

    result = relationship(
        "Result",
        back_populates="templates_result",
        foreign_keys=[IDExport],
        primaryjoin="Result.IDExport == TemplatesResult.IDExport",
    )
    template_sms = relationship(
        "TemplateSMS",
        back_populates="templates_result",
        foreign_keys=[template_id],
        primaryjoin="TemplateSMS.id == TemplatesResult.template_id",
    )

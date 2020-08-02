"""
Define modelos de validação para Logs
"""
from datetime import datetime

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class LogBase(BaseModel):
    """
    LogBase define campos que estão presentes na criação e na
    visualização de um Log
    """

    client_date_time: datetime
    results_id: int = None
    user_id: int = None
    client_ip: str = None
    message: str


class LogCreate(LogBase):
    """
    LogCreate define os campos necessários ao criar um Log.
    São os mesmo de LogBase
    """

    pass


class Log(LogBase):
    """
    Log define uma estrutura geral para Log
    """

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Metadata to define the orm_mode of sqlalchemy
        """

        orm_mode = True

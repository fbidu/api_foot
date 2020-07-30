"""
Schema for PDF processing response
"""
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class PDFProcessed(BaseModel):
    """
    Contains metadata about a processed PDF file
    """

    length: int
    sha256: str
    filename: str

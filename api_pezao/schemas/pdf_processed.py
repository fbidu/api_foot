"""
Schema for PDF processing response
"""
from pydantic import BaseModel


class PDFProcessed(BaseModel):
    """
    Contains metadata about a processed PDF file
    """

    length: int
    sha256: str
    filename: str

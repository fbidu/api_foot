"""
Module that offers a basic settings management
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Offers settings for all the API

    Attributes:

        pdf_storage_path: (string) The path where PDF files should be saved
    """

    pdf_storage_path: str = "/tmp"


settings = Settings()

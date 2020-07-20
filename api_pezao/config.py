"""
Module that offers a basic settings management
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Offers settings for all the API

    Attributes:

        pdf_storage_path: (string) The path where PDF files should be saved

        sms_sweep_time: (string) Programmed daily SMS sending time. Cron Time Format.

        daily_sms_sweep_active: (boolean) Defines if daily SMS sending are active (True) or not (False)
    """

    pdf_storage_path: str = "/tmp"
    sms_sweep_time: str = "0 10 * * *"
    daily_sms_sweep_active: bool = True

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

        daily_sms_sweep_active: (boolean) Defines if daily SMS sending are
            active (True) or not (False)
    """

    pdf_storage_path: str = "/tmp"
    upload_secret: str = "c99b3e00f5215e1e103d9358a77435f0014c2d589b37fac8c417aafd351067bd"

    sms_username: str = "FUNCAMP02"
    sms_password: str = "Pezao$2020"
    sms_sweep_time: str = "0 10 * * *"
    daily_sms_sweep_active: bool = True
    sms_active: bool = False
    postgres_url: str = None
    valid_ddd: set = [
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "21",
        "22",
        "24",
        "27",
        "28",
        "31",
        "32",
        "33",
        "34",
        "35",
        "37",
        "38",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "51",
        "53",
        "54",
        "55",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "71",
        "73",
        "74",
        "75",
        "77",
        "79",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "91",
        "92",
        "93",
        "94",
        "95",
        "96",
        "97",
        "98",
        "99",
    ]

"""
Function send_sms: sends SMS
"""

import re
import logging
from typing import List

from requests import post
from sqlalchemy.orm import Session

from . import config, log, crud


def send_sms(number, text, msg_id=0, settings=None):
    """
    Another send sms
    """
    if not settings:
        settings = config.Settings()

    if not settings.sms_active:
        log(
            f"Pedido de envio de SMS para {number} mas o SMS está desabilitado!",
            level=logging.WARNING,
        )

    payload = {
        "NumUsu": settings.sms_username,
        "Senha": settings.sms_password,
        "SeuNum": msg_id,
        "Celular": number,
        "Mensagem": text,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    url = "https://webservices.twwwireless.com.br/reluzcap/wsreluzcap.asmx/EnviaSMS"
    response = post(url, data=payload, headers=headers)

    return (
        response.status_code == 200
        and "NOK" not in response.text
        and "OK" in response.text
    )


def verify_phone(number: str, settings: config.Settings = None):
    """
    Verifies if a string in the list is a valid brazilian mobile number
    Returns the same string if valid, or an error code string if invalid
    Error Code 0 - not a phone number
    Error Code 1 - not a mobile number (maybe a land line)
    Error Code 2 - mobile number with invalid ddd

    >>> verify_phone("sem fone")
    0

    >>> verify_phone("")
    0

    >>> verify_phone("000000000000000")
    1

    >>> verify_phone("11 39289524")
    1

    >>> verify_phone("1139289524")
    1

    >>> verify_phone("23 995322524")
    2

    >>> verify_phone("23 995322524")
    2

    >>> verify_phone("19 995322524")
    '19995322524'

    >>> verify_phone("19 99532-2524")
    '19995322524'

    >>> verify_phone("19995322524")
    '19995322524'

    """

    if not settings:
        settings = config.Settings()

    # removes all non-digits from phone number string
    number = re.sub("[^0-9]", "", number)

    # if there are no numbers on the phone string,
    # it isn't a phone (error code 0)
    if not number:
        return 0

    # if the first digit of the number itself is less than 6,
    # it's not a cellphone number (error code 2)
    if int(number[2]) < 6:
        return 1

    # if the ddd doesn't match any valid ddd, the number doesn't have a valid ddd (error code 1)
    if number[:2] not in settings.valid_ddd:
        return 2

    # if there are no errors, the number is valid
    return number


def sms_intermediary(hospitals: List[str], db: Session):
    """
    Intermediary SMS-sending function, gets the necessary data, calls necessary functions, does log
    """
    sms_list = crud.sms_sweep(db, hospitals)

    for sms in sms_list:
        if sms[0] == "0":
            log(f"ERRO: resultado de id {sms[2]} não possui número de telefone.", db)
            continue
        if sms[0] == "1":
            log(f"ERRO: resultado de id {sms[2]} não possui um número de celular.", db)
            continue
        if sms[0] == "2":
            log(f"ERRO: DDD inválido no celular do resultado de id {sms[2]}.", db)
            continue

        sms_successful = send_sms(sms[0], sms[1])

        if sms_successful:
            log(f"SMS do resultado {sms[2]} enviado para {sms[0]} com sucesso.", db)
            continue
        log(f"ERRO: No envido o SMS do resultado {sms[2]} para {sms[0]}.", db)

"""
Function send_sms: sends SMS
"""

import re

from requests import post

from . import config
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends

from . import config, log, crud


def send_sms(number: str, text: str):
    """
    Sends SMS
    """
    if True:
        print("SMS Sent!")
        return True

    print("SMS Failed.")
    return False


def send_sms1(number, text, msg_id=0, settings=None):
    """
    Another send sms
    """
    if not settings:
        settings = config.Settings()

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
            log(
                "ERRO: resultado de id %s não possui número de telefone." % str(sms[2]),
                db,
            )
        elif sms[0] == "1":
            log(
                "ERRO: resultado de id %s não possui um número de telefone celular."
                % str(sms[2]),
                db,
            )
        elif sms[0] == "2":
            log(
                "ERRO: DDD inválido no número de celular do resultado de id %s."
                % str(sms[2]),
                db,
            )

        else:
            if send_sms(sms[0], sms[1]):
                log(
                    "SMS do resultado de id %s enviado para número %s com sucesso."
                    % (str(sms[2]), sms[0]),
                    db,
                )
                if not crud.confirm_sms(db, sms[2]):
                    log(
                        "ERRO: Ocorreu um erro confirmando o envio do SMS do resultado de id %s"
                        % (str(sms[2])),
                        db,
                    )

            else:
                log(
                    "ERRO: Não foi possível enviar o SMS do resultado de id %s para o número %s."
                    % (str(sms[2]), sms[0]),
                    db,
                )
    return

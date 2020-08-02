"""
SMS CRUD
"""

from collections import namedtuple
from typing import List

from sqlalchemy.orm import Session

from .. import models, sms_utils
from ..models import Result

VerificationResult = namedtuple("VerificationResult", ["valid_phones", "error_codes"])


def lists_unsent_sms(db: Session, hospital_list: List[str] = None):
    """
    Lista todos os SMSs que precisam ser enviados. Se um argumento hospital_list
    for oferecido contendo o COD_LocColeta de uma unidade, apenas os SMSs
    daquelas unidades são considerados.
    """
    unsent_sms = db.query(models.Result).filter(~models.Result.sms_sent)
    if hospital_list:
        return unsent_sms.filter(models.Result.COD_LocColeta.in_(hospital_list)).all()
    return unsent_sms.all()


def verify_result_phones(result: Result) -> VerificationResult:
    """
    Dado um resultado, retorna o estado de validade de seus telefones
    """
    # checks if there are valid mobile phone numbers for sending SMS on that result.
    # valid numbers are saved to the valid_phones list
    # error codes (0: no phones, 1: no mobile phones, 2: invalid ddd)
    # are saved on error_codes list

    if not (result.ptnPhone1 or result.ptnPhone2):
        return VerificationResult([], [])

    result_phones = [phone for phone in (result.ptnPhone1, result.ptnPhone2) if phone]
    error_codes = []
    valid_phones = []

    for phone in result_phones:
        verification_code = sms_utils.verify_phone(phone)
        if isinstance(verification_code, int):
            error_codes.append(verification_code)
        else:
            valid_phones.append(verification_code)

    return VerificationResult(valid_phones, error_codes)


def sms_sweep(db: Session, hospital_list: List[str] = None):
    """
    Returns a (phone, message, result id) for every SMS that needs to be sent
    If a list of hospitals is provided, returns SMSs to be sent from exams made
    in those hospitals only
    """

    result_list = lists_unsent_sms(db, hospital_list)

    # creates a list of SMS to be returned
    # every entry in the list is a tuple (phone, message)
    sms_list = []

    for result in result_list:

        valid_phones = []
        error_codes = []

        validation = verify_result_phones(result)
        valid_phones.extend(validation.valid_phones)
        error_codes.extend(validation.error_codes)

        # if there are no valid numbers, report back the gravest error found (smaller number)
        if not valid_phones:
            if error_codes:
                error_codes.sort()
                sms_list.append((str(error_codes[0]), None, result.id))
            else:
                sms_list.append(("0", None, result.id))

        else:
            # if there are valid phones...

            # find the sms message to be sent:
            # look in the template_results table for the entry with same
            # result_id as the result's id
            # then, look in the template_sms table for the entry with same
            # id as the discovered
            # template_results' template_id
            for message in result.templates_result:
                for phone in valid_phones:
                    sms_list.append((phone, message.template_sms.msg, result.id))

    return sms_list


def confirm_sms(db: Session, result_id):
    """
    Registra que o sms de um resultado foi enviado
    """
    db_result = db.query(models.Result).filter(models.Result.id == result_id).first()
    db_result.sms_sent = True

    db.commit()
    db.refresh(db_result)

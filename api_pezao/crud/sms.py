from typing import List
from sqlalchemy.orm import Session

from .. import models, sms_utils


def sms_sweep(db: Session, hospital_list: List[str] = None):
    """
    Returns a (phone, message, result id) for every SMS that needs to be sent
    If a list of hospitals is provided, returns SMSs to be sent from exams made in those hospitals only
    """

    if not hospital_list:
        # no defined hospitals -> return every result which SMS hadn't been sent yet
        result_list = db.query(models.Result).filter(~models.Result.sms_sent).all()
    else:
        # defined hospitals -> return not sent results whose hospital code is in hospitals list
        result_list = (
            db.query(models.Result)
            .filter(
                ~models.Result.sms_sent, models.Result.COD_LocColeta.in_(hospital_list)
            )
            .all()
        )

    # creates a list of SMS to be returned
    # every entry in the list is a tuple (phone, message)
    sms_list = []

    # for each result that needs SMS to be sent:
    for result in result_list:

        valid_phones = []
        error_codes = []

        # checks if there are valid mobile phone numbers for sending SMS on that result.
        # valid numbers are saved to the valid_phones list
        # error codes (0: no phones, 1: no mobile phones, 2: invalid ddd) are saved on error_codes list

        result_phones = [result.ptnPhone1, result.ptnPhone2]
        if result_phones:
            for phone in [result.ptnPhone1, result.ptnPhone2]:
                if phone:
                    v = sms_utils.verify_phone(phone)
                    if isinstance(v, int):
                        error_codes.append(v)
                    else:
                        valid_phones.append(v)

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
            # look in the template_results table for the entry with same result_id as the result's id
            # then, look in the template_sms table for the entry with same id as the discovered
            # template_results' template_id
            for message in result.templates_result:
                for phone in valid_phones:
                    sms_list.append((phone, message.template_sms.msg, result.id))

    # returns list of sms messages to be sent
    return sms_list


def confirm_sms(db: Session, result_id):
    db_result = db.query(models.Result).filter(models.Result.id == result_id)
    db_result.sms_sent = True

    db.commit()
    db.refresh(db_result)
    return True

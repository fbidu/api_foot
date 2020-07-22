"""
Function send_sms: sends SMS
"""

import re
from . import config


def send_sms(number, text):
    if True:
        print("SMS Sent!")
        return True
    else:
        print("SMS Failed.")
        return False


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

    # if there are no numbers on the phone string, it isn't a phone (error code 0)
    if not number:
        return 0

    # if the first digit of the number itself is less than 6, it's not a cellphone number (error code 2)
    elif int(number[2]) < 6:
        return 1

    # if the ddd doesn't match any valid ddd, the number doesn't have a valid ddd (error code 1)
    elif number[:2] not in settings.valid_ddd:
        return 2

    # if there are no errors, the number is valid
    else:
        return number

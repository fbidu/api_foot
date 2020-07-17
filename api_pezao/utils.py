"""
Utilitary functions for the API
"""
import hashlib
import re


def sha256(path):
    """
    Hashes a file in chunks
    """
    hash_256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_256.update(chunk)
    return hash_256.hexdigest()


def is_valid_email(candidate: str) -> bool:
    """
    Returns if a string is a valid email address

    >>> is_valid_email("test@test.com")
    True

    >>> is_valid_email("test@gmail.com")
    True

    >>> is_valid_email("test.test@test.com.br")
    True

    >>> is_valid_email("test.test@test.nice.subdomain.com")
    True

    >>> is_valid_email("test+test@test.com")
    True
    """
    return bool(
        re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", candidate)
    )


def is_valid_cpf(candidate: str) -> bool:
    """
    Returns if a string is a valid CPF number

    >>> is_valid_cpf("00000000000")
    True

    >>> is_valid_cpf("000.000.000-00")
    True
    """

    candidate = re.findall(r"\d", candidate)

    if not len(candidate) == 11:
        return False

    return True

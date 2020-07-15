"""
Módulo que provê funções de autenticação
"""


from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password):
    """
    Verifica se uma senha é igual à versão hasheada.

    Argumentos:
        plain_password (str): a senha em texto puro para ser verificada
        hashed_password (str): a senha hasheada

    >>> verify_password("teste", '$2b$12$EaNbYtDQU1M25UTtwoe3nO36bZUjAtla4mCT5vJph8JhBOK3X/bd6')
    True
    """

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Dada uma senha, retorna sua versão hasheada. A senha hasheada
    pode ser verificada com `verify_password`

    >>> pwd = "test"
    >>> hashed = get_password_hash(pwd)
    >>> verify_password(pwd, hashed)
    True

    """
    return pwd_context.hash(password)

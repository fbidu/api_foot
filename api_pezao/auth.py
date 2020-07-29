"""
Módulo que provê funções de autenticação
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = "5e268048c43da6bab86bfa68c9166380fac82474b9c4ed0c62317d2d7fc1f031"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT token


    >>> from jose import jwt
    >>> token = create_access_token({"name": "test"})
    >>> jwt.get_unverified_claims(token)["name"]
    'test'
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
Módulo que provê funções de autenticação
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retorna informações do usuário logado
    """
    return token * 2

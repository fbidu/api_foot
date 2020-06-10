"""
Testa se as configurações estão disponíveis
"""

from pytest import fixture
from api_pezao.main import get_settings

# pylint: disable=redefined-outer-name


@fixture
def settings():
    """
    Returns a new setting instance
    """
    return get_settings()


def test_settings_keys(settings):
    """
    Testa se as chaves esperadas estão definidas
    """
    assert "pdf_storage_path" in settings.dict()

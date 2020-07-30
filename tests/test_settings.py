"""
Testa se as configurações estão disponíveis
"""
from os import environ
from pytest import fixture
from api_pezao.config import Settings
from api_pezao.deps import get_settings

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


def test_settings_obey_environment_var():
    """
    Testa se as configurações de ambiente modificam o storage de PDF
    """
    environ["pdf_storage_path"] = "test"
    settings = Settings()

    assert settings.pdf_storage_path == "test"

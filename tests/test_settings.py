"""
Testa se as configurações estão disponíveis
"""

from api_pezao import settings


def test_settings_keys():
    """
    Testa se as chaves esperadas estão definidas
    """
    assert "pdf_storage_path" in settings.dict()

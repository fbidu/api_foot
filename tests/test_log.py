"""
Teste unitário para log
"""
from api_pezao import crud, log


def test_log_works(db):
    """
    Teste de log simples
    """
    log("test!!", db=db, override_test=True)

    assert len(crud.list_logs(db)) != 0

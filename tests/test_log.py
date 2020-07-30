from api_pezao import crud, log


def test_log_works(db):
    log("test!!", db=db)

    assert len(crud.list_logs(db)) == 1

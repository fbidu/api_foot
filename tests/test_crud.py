"""
Testes unitários para as funções de banco de dados
"""
from warnings import resetwarnings
from pytest import fixture
from sqlalchemy.orm import Session

from api_pezao import crud
from api_pezao.models import User, TemplateSMS, TemplatesResult, Result

from .db_utils import create_test_user

# pylint: disable=redefined-outer-name


@fixture
def test_user(db) -> User:
    """
    Cria um usuário de teste para ser usado nas funções abaixo
    """
    return create_test_user(db)


def test_find_user_by_email(db: Session, test_user: User):
    """
    Testa se conseguimos encontrar um usuário por email
    """
    found_user = crud.find_user(db, username="test@test.com")

    assert found_user
    assert test_user == found_user


def test_find_user_by_cpf(db: Session, test_user: User):
    """
    Testa se conseguimos encontrar um usuário por cpf
    """
    found_user = crud.find_user(db, username="00000000000")

    assert found_user
    assert test_user == found_user
<<<<<<< HEAD
=======


def test_find_user_by_both_cpf_and_email(db: Session, test_user: User):
    """
    Testa se conseguimos encontrar um usuário por cpf
    """

    found_user = crud.find_user(db, cpf="00000000000", email="test@test.com")

    assert found_user
    assert test_user == found_user

    found_user = crud.find_user(db, cpf="00000000000", email="email-errado")
    assert not found_user

    found_user = crud.find_user(db, cpf="123456", email="test@test.com")
    assert not found_user


def test_find_user_without_args_returns_none(db: Session):
    """
    Testa se conseguimos encontrar um usuário por email
    """
    found_user = crud.find_user(db)

    assert not found_user
    assert found_user is None


def test_sms_sweep(db: Session):
    """
    Testa se o sweep de SMS funciona bem
    """

    db_result = Result(sms_sent=False, ptnPhone1="19981140000")
    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    template_sms = TemplateSMS(msg="test")
    db.add(template_sms)
    db.commit()
    db.refresh(template_sms)

    template_result = TemplatesResult(result=db_result, template_sms=template_sms)
    db.add(template_result)
    db.commit()

    messages_to_sent = crud.sms_sweep(db)

    assert len(messages_to_sent) == 1

    message_to_sent = messages_to_sent[0]
    assert len(message_to_sent) == 3
    assert message_to_sent[0] == db_result.ptnPhone1
    assert message_to_sent[1] == template_sms.msg
    assert message_to_sent[2] == db_result.id
>>>>>>> 923bd3b... Add tests

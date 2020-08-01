"""
Testes unitários para o módulo de leitura de CSV
"""
from csv import DictReader
from pathlib import Path

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError

from api_pezao import csv_input
from api_pezao.crud.result import read_results
from api_pezao.crud.user import list_users
from api_pezao.models import TemplatesResult, TemplateSMS


def import_test_results(db):
    """
    Função auxiliar de importação de CSV
    """
    sample_file = Path("tests/demo.csv").absolute()
    content = open(sample_file)
    return csv_input.import_results_csv(content, db)


def test_import_results_csv(db):
    """
    testa se a função de import_csv retorna o total correto de linhas
    """

    imported_objects = import_test_results(db)
    assert len(imported_objects) == 111

    db_results = read_results(db)
    assert len(db_results) == 111

    # assert len(list_users(db)) == 159


def test_import_templates_results_csv(db):
    """
    Testa se a importação da relação results-templates funciona
    """
    sample_file = Path("tests/demo_templates_result.csv").absolute()
    content = open(sample_file)
    results = import_test_results(db)
    assert len(csv_input.import_templates_results_csv(content, db)) == 111

    db_objects = db.query(TemplatesResult).all()

    assert len(db_objects) == 111

    template_sms_0 = db_objects[0]

    assert template_sms_0.template_id == 1
    assert template_sms_0.IDExport == results[0].IDExport
    assert template_sms_0.result.IDExport == results[0].IDExport

    db_template = TemplateSMS(id=1, msg="test")
    db.add(db_template)
    db.commit()
    db.refresh(db_template)

    assert template_sms_0.template_sms.msg == db_template.msg


def test_csv_to_pydantic():
    """
    Testa se a conversão csv-pydantic funciona
    """

    class User(BaseModel):
        """
        Test class for the import
        """

        # pylint: disable=no-self-argument,missing-function-docstring,no-self-use
        name: str
        age: int = 0

        @validator("name")
        def name_not_empty(cls, value):
            if not value:
                raise ValidationError("Name canot be empty")
            return value

    csv_data = "name,age\ntest1,10\ntest2,\ntest3,20\n,40"

    reader = DictReader(csv_data.split("\n"))

    csv_to_pydantic_result = csv_input.csv_to_pydantic(reader, User)
    assert csv_to_pydantic_result

    assert len(csv_to_pydantic_result.objects) == 3
    assert len(csv_to_pydantic_result.errors) == 1

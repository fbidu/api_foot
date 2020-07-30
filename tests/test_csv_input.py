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


def test_import_csv(db):
    """
    testa se a função de import_csv retorna o total correto de linhas
    """
    sample_file = Path("tests/demo.csv").absolute()
    content = open(sample_file)
    assert csv_input.import_csv(content, db) == 159

    db_results = read_results(db)
    assert len(db_results) == 159


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

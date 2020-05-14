"""
Testes unitários para o módulo de leitura de CSV
"""
from pathlib import Path
from api_pezao import csv_input


def test_import_csv():
    """
    testa se a função de import_csv retorna o total correto de linhas
    """
    sample_file = Path("tests/demo.csv").absolute()
    content = open(sample_file)
    assert csv_input.import_csv(content) == 4

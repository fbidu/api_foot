"""
Teste unitário para carga de PDF
"""
from os import remove
from pathlib import Path
from random import randint
from api_pezao import pdf_input


def test_pdf_input():
    """
    Testa se o arquivo PDF é salvo no lugar certo
    """
    sample_file = Path("tests/demo.pdf").absolute()
    target = Path(f"/tmp/test_pezao_{randint(1, 1000)}.pdf")
    content = open(sample_file, "rb")
    pdf_input.save_pdf(content, target)

    assert target.exists()
    remove(target.absolute())

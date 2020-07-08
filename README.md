# Pezão API

A API principal do projeto

## Ambiente de Desenvolvimento

Para rodar a API em desenvolvimento você precisará de:

* Python >= 3.8
* [Poetry](https://python-poetry.org/docs/#installation)

Clone esse repositório e execute dentro da pasta

`poetry install`

Após o processo, você deverá ser capaz de rodar o projeto com

`poetry run uvicorn api_pezao.main:app --reload --debug`


### Adicionais

Além do Poetry, esse projeto também define o uso do [`Pylint`](https://www.pylint.org/) como verificador
estático de código e do [`black`](https://github.com/psf/black) como formatador automático.

Esses dois projetos podem ser executados manualmente mas, adicionalmente, você
pode instalar o `[pre-commit]'(https://pre-commit.com/) também.

## Rodando

### Configurações

* `pdf_storage_path`: Caminho completo para onde os PDFs dos laudos devem ser
  salvos e buscados

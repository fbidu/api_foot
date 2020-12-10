# API

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

### Com Docker

O projeto inclui um `Dockerfile` que permite a criação de imagens docker
para hospedagem da aplicação.

1. **Monte a imagem** com `docker build . -t pezao` ― esse comando irá criar
   uma imagem marcada com a tag `pezao` em seu sistema

2. **Execute a imagem** com `docker run -p 8000:8000 --rm pezao` ― esse comando vai fazer
   uma execução básica da imagens, para testes. A instrução `-p 8000:8000` irá
   plugar a porta 8000 da máquina hospedeira na porta 8000 da imagem. Isso vai
   permitir que você teste a aplicação chamando `localhost` em si.

3. **Montando volumes** ― Para que o docker persista os arquivos que ele recebe,
   é necessário montar um volume. A forma mais fácil de fazer isso é

   ```bash
   docker run -v <caminho_local>:<caminho_na_imagem> -p 8000:8000 pezao
   ```

   Por exemplo, para montar a pasta `/home/ubuntu/data` na pasta `/tmp` remota,
   o comando é:

   ```bash
   docker run -v /home/ubuntu/data:/tmp -p 8000:8000 pezao
   ```

   Em sistemas RHEL ― Fedora, CentOS, etc ― pode ser necessário adicionar a flag
   `z` ao final para dar as permissões corretas.
   [info](https://www.projectatomic.io/blog/2015/06/using-volumes-with-docker-can-cause-problems-with-selinux/)

   ```bash
   docker run -v /home/ubuntu/data:/tmp:z -p 8000:8000 pezao
   ```

4. **Mudando Configurações** ― Todas as configurações em `config.py` podem ser customizadas
   com variáveis de ambiente do mesmo nome. Você pode definir variáveis de ambiente
   em docker com a flag `-e`. Por exemplo, para customizar o caminho de salvar
   PDFs para `/data`, o caminho é:

   ```bash
   docker run -e PDF_STORAGE_PATH=/data -p 8000:8000 pezao
   ```

   Você pode confirmar que a configuração foi lida através da saída do comando:

   ```txt
    (...)
    INFO:     As configurações são {
      "daily_sms_sweep_active": true,
      "pdf_storage_path": "/data",
    (...)
   ```

### Configurações

* `pdf_storage_path`: Caminho completo para onde os PDFs dos laudos devem ser
  salvos e buscados

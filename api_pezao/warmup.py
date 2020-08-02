"""
Warmup functions
"""
from getpass import getpass
from pathlib import Path

import requests

# pylint: disable=invalid-name


class Warmup:
    """
    Classe com funções de warmup
    """

    def __init__(self, api_url, upload_secret):
        self.api_url = api_url
        self.headers = {"authorization": upload_secret}

    def _import_csv(self, filename, type_):
        files = {"csv_file": open(filename, "r")}

        response = requests.post(
            f"{self.api_url}/csv/?type={type_}", files=files, headers=self.headers
        )

        if response.status_code > 399:
            return response

        return response.json()

    def import_results(self, filename):
        """
        Import CSV de resultados
        """
        return self._import_csv(filename, type_="results")

    def import_templates_results(self, filename):
        """
        Import CSV de templates_results
        """
        return self._import_csv(filename, type_="templates_results")

    def import_hospitals(self, filename):
        """
        Importa CSV de hospitais
        """
        return self._import_csv(filename, type_="hospitals")

    def create_super_user(self, name, email, password):
        """
        Creates a new user
        """
        data = {
            "name": name,
            "email": email,
            "password": password,
            "is_superuser": True,
            "is_staff": True,
        }
        response = requests.post(
            f"{self.api_url}/users/", headers=self.headers, json=data
        )

        return response.json()

    def import_pdf(self, folder_path: str):
        """
        Imports all the PDFs of a folder
        """
        folder = Path(folder_path)
        failures = 0
        successes = 0
        for file in folder.glob("*.pdf"):
            print(f"Processando {file.absolute()}")
            files = {"pdf_file": open(file.absolute(), "rb")}
            result = requests.post(
                f"{self.api_url}/pdf/", headers=self.headers, files=files
            )

            if result.status_code > 399:
                print(f"Falha ao processar {file.absolute()}")
                failures += 1
            else:
                print(f"Processado com sucesso {file.absolute()}")
                successes += 1
        return f"{successes} PDFs Importados com sucesso. {failures} falhas"


def process_option(option_, *args, **kwargs):
    """
    Processa a opção pedida
    """
    if option_ == "q":
        return "Até mais!"

    options = {
        "1": warm.import_results,
        "2": warm.import_templates_results,
        "5": warm.import_hospitals,
    }

    if option_ in ("1", "2", "5"):
        filename = input("Digite o caminho completo do arquivo: ")

        return options[option_](filename=filename, *args, **kwargs)
    if option == "3":
        name = input("Digite o nome do usuário ")
        email = input("Digite o email do usuário ")
        senha = getpass("Digite a senha: ")

        return warm.create_super_user(name, email, senha)

    if option == "4":
        folder_path = input("Digite o caminho completo da pasta com PDFs: ")
        confirm = input(
            f"Todos os arquivos PDFs de {folder_path} serão importados. Continuar? [s/n]"
        )

        if confirm.lower() == "s":
            return warm.import_pdf(folder_path)
        return "Opção inválida."

    return "Erro"


if __name__ == "__main__":
    url = input("Digite a URL da API [http://127.0.0.1:8000]: ")
    if not url:
        url = "http://127.0.0.1:8000"

    upload_secret_ = input("Digite o upload secret da API: ")

    warm = Warmup(url, upload_secret_)

    option = None

    while option != "q":
        print(
            """
        Digite uma opção:

        [1] Importar Resultados
        [2] Importar Templates Results
        [3] Criar Super Usuário
        [4] Importar PDFs
        [5] Importar Hospitais
        [q] Sair
        """
        )

        option = input("> ")

        print(process_option(option))

"""
Warmup functions
"""
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


def process_option(option_, *args, **kwargs):
    """
    Processa a opção pedida
    """
    if option_ == "q":
        return "Até mais!"

    options = {"1": warm.import_results, "2": warm.import_templates_results}

    if option_ in ("1", "2"):
        filename = input("Digite o caminho completo do arquivo: ")

        return options[option_](filename=filename, *args, **kwargs)

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

        [1] Importar resultados
        [2] Importar Templates Results
        [q] Sair
        """
        )

        option = input("> ")

        print(process_option(option))

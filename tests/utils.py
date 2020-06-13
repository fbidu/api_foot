"""
Utilitary function to aid testing
"""
from api_pezao.utils import sha256


def check_files_equal(path_a, path_b):
    """
    Checks if two files are equal
    """

    return sha256(path_a) == sha256(path_b)


def post_pdf(sample_pdf, client):
    """
    Posts a file to the main PDF endpoint
    """
    files = {"pdf_file": open(sample_pdf, "rb")}
    return client.post("/pdf/", files=files)

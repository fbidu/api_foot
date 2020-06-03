"""
Module that handles PDF files
"""


def save_pdf(content, path):
    """
    Saves the content of a PDF file in Path
    """
    with open(path, "wb") as target:
        target.write(content.read())

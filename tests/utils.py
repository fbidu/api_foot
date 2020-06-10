"""
Utilitary function to aid testing
"""
import hashlib


def check_files_equal(path_a, path_b):
    """
    Checks if two files are equal
    """

    def sha256(path):
        """
        Hashes a file in chunks
        """
        hash_256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_256.update(chunk)
        return hash_256.hexdigest()

    return sha256(path_a) == sha256(path_b)

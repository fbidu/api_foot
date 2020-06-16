"""
Utilitary functions for the API
"""
import hashlib


def sha256(path):
    """
    Hashes a file in chunks
    """
    hash_256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_256.update(chunk)
    return hash_256.hexdigest()

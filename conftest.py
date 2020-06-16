"""
Provides fixtures for Pytest tests
"""
from fastapi.testclient import TestClient
from pytest import fixture
from api_pezao import main


@fixture
def client():
    """
    Offers a test client for the main API
    """
    return TestClient(main.app)

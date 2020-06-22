"""
Provides fixtures for Pytest tests
"""
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_pezao import main
from api_pezao.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Overrides the default db for testing
    """
    # pylint: disable=no-member
    try:
        connection = engine.connect()
        transaction = connection.begin()
        session = TestingSessionLocal(bind=connection)
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@fixture
def client():
    """
    Offers a test client for the main API
    """
    main.app.dependency_overrides[main.get_db] = override_get_db
    return TestClient(main.app)

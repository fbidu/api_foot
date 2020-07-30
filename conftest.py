"""
Provides fixtures for Pytest tests
"""
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_pezao import deps, main
from api_pezao.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@fixture
def db():
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


# pylint: disable=redefined-outer-name
@fixture
def client(db):
    """
    Offers a test client for the main API
    """

    def __get_db_fixture():
        return db

    main.app.dependency_overrides[deps.get_db] = __get_db_fixture

    return TestClient(main.app)

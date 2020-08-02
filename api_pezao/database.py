"""
Provides SQLAlchemy connectivity to the rest of the app
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Settings

POSTGRES_URL = Settings().postgres_url

SQLALCHEMY_DATABASE_URL = POSTGRES_URL if POSTGRES_URL else "sqlite:///./sql_app.db"

CONNECT_ARGS = {} if POSTGRES_URL else {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=CONNECT_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

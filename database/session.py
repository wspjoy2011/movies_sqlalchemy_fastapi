from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from config import settings
from database.listeners import movies # noqa: F401

engine = create_engine(f'sqlite:///{settings.PATH_TO_DB}', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

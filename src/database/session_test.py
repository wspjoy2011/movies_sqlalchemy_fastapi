from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.base import Base

SQLITE_URL = "sqlite+aiosqlite:///:memory:"
sqlite_engine = create_async_engine(SQLITE_URL, echo=False)
AsyncSQLiteSessionLocal = sessionmaker(bind=sqlite_engine, class_=AsyncSession, expire_on_commit=False)


async def get_sqlite_session() -> AsyncSession:
    """
    Provides an asynchronous session for SQLite database.
    Yields:
        AsyncSession: An active asynchronous session for SQLite.
    """
    async with AsyncSQLiteSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_sqlite_session_context() -> AsyncSession:
    """
    Provides an asynchronous session for SQLite using a context manager.

    Yields:
        AsyncSession: An active asynchronous SQLite session.
    """
    generator = get_sqlite_session()
    session = await generator.__anext__()
    try:
        yield session
    finally:
        await generator.aclose()


async def setup_sqlite_database():
    """
    Creates all tables in the SQLite database.
    """
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_sqlite_database():
    """
    Drops and recreates all tables in the SQLite database.
    This ensures the database is reset before each test.
    """
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

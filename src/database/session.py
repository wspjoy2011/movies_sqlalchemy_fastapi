from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config.dependencies import get_settings
from database.listeners import movies # noqa: F401

settings = get_settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_DB_PORT}/{settings.POSTGRES_DB}"
DATABASE_URL_SYNC = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_DB_PORT}/{settings.POSTGRES_DB}"

engine_sync = create_engine(DATABASE_URL_SYNC, echo=True)
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_session_context() -> AsyncSession:
    """
    Provides an asynchronous session for use in scripts or standalone contexts.

    This function wraps the existing `get_session` generator to allow its use
    as a standard async context manager.

    Yields:
        AsyncSession: An active asynchronous database session.
    """
    generator = get_session()
    session = await generator.__anext__()
    try:
        yield session
    finally:
        await generator.aclose()



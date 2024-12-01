from aioredis import Redis, from_url
from fastapi import Depends
from pydantic_settings import BaseSettings

from config.settings import Settings


def get_settings() -> BaseSettings:
    """
    Retrieve the application settings.

    Returns:
        BaseSettings: The settings instance, providing configuration values for the application.
    """
    return Settings()


async def get_redis_connection(settings: Settings = Depends(get_settings)) -> Redis:
    """
    Create an asynchronous Redis connection.

    Args:
        settings (Settings): The application settings, injected via dependency.

    Returns:
        Redis: An active Redis connection.

    Raises:
        RedisError: If the connection to the Redis server fails.
    """
    return await from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )

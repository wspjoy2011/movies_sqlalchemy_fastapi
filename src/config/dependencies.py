from fastapi import Depends
from aioredis import Redis
from pydantic_settings import BaseSettings


from config.settings import Settings
from cache import (
    get_redis_connection,
    CacheManagerInterface,
    RedisCacheManager,
    RedisConnectionSettingsDTO
)


def get_settings() -> BaseSettings:
    """
    Retrieve the application settings.

    Returns:
        BaseSettings: The settings instance, providing configuration values for the application.
    """
    return Settings()


def _get_redis_connection_settings(settings: Settings = Depends(get_settings)) -> RedisConnectionSettingsDTO:
    """
    Dependency to retrieve Redis connection settings as a DTO.

    Args:
        settings (Settings): Application settings.

    Returns:
        RedisConnectionSettingsDTO: Redis connection settings.
    """
    return RedisConnectionSettingsDTO(
        REDIS_HOST=settings.REDIS_HOST,
        REDIS_PASSWORD=settings.REDIS_PASSWORD,
        REDIS_PORT=settings.REDIS_PORT,
    )


async def _get_redis_connection_instance(
    settings_dto: RedisConnectionSettingsDTO = Depends(_get_redis_connection_settings),
) -> Redis:
    """
    Dependency to create and return an asynchronous Redis connection.

    Args:
        settings_dto (RedisConnectionSettingsDTO): Redis connection settings DTO.

    Returns:
        Redis: An active Redis connection instance.
    """
    return await get_redis_connection(settings_dto)


def get_cache_manager(
    redis: Redis = Depends(_get_redis_connection_instance),
) -> CacheManagerInterface:
    """
    Dependency to create and return a cache manager instance.

    Args:
        redis (Redis): An active Redis connection instance.

    Returns:
        CacheManagerInterface: A cache manager instance.
    """
    return RedisCacheManager(redis)

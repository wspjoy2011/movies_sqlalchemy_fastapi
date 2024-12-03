from aioredis import Redis, from_url

from cache import RedisConnectionSettingsDTO, CacheConnectionError


async def get_redis_connection(settings: RedisConnectionSettingsDTO, decode_responses: bool = True) -> Redis:
    """
    Create an asynchronous Redis connection.

    Args:
        settings (RedisConnectionSettingsDTO): DTO containing Redis connection details.
        decode_responses (bool): Whether to decode responses to string format. Defaults to True.

    Returns:
        Redis: An active Redis connection.

    Raises:
        RedisConnectionError: If the connection to the Redis server fails.
    """
    try:
        return await from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            password=settings.REDIS_PASSWORD,
            decode_responses=decode_responses
        )
    except ConnectionError as e:
        raise CacheConnectionError(f"Could not connect to Redis: {str(e)}") from e

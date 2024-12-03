import json

from aioredis import Redis, RedisError

from cache import CacheBaseError, CacheManagerInterface,json_serializer


class RedisCacheManager(CacheManagerInterface):
    """
    Class to manage Redis cache operations using the aioredis library.

    Provides methods for setting, retrieving, deleting, and clearing cache entries.
    """

    def __init__(self, redis: Redis):
        """
        Initializes a connection to the Redis server.

        Args:
            redis (Redis): An active Redis connection instance.
        """
        self._redis = redis

    async def set(self, key: str, value: dict, expiration: int = 3600) -> None:
        """
        Caches data with a specified expiration time.

        Args:
            key (str): The key under which the data will be cached.
            value (dict): The data to be cached, serialized into JSON format.
            expiration (int): Time-to-live for the cache key in seconds. Defaults to 3600 seconds (1 hour).

        Raises:
            CacheBaseError: If an error occurs while interacting with Redis.
        """
        try:
            await self._redis.set(key, json.dumps(value, default=json_serializer), ex=expiration)
        except RedisError as e:
            raise CacheBaseError(f"Failed to set cache for key {key}: {e}") from e

    async def get(self, key: str) -> dict:
        """
        Retrieves data from the cache.

        Args:
            key (str): The cache key to retrieve.

        Returns:
            dict: The cached data deserialized from JSON if the key exists, otherwise None.

        Raises:
            CacheBaseError: If an error occurs while interacting with Redis.
        """
        try:
            data = await self._redis.get(key)
            return json.loads(data) if data else None
        except RedisError as e:
            raise CacheBaseError(f"Failed to get cache for key {key}: {e}") from e

    async def delete(self, key: str) -> None:
        """
        Deletes a specific cache entry by key.

        Args:
            key (str): The cache key to delete.

        Raises:
            CacheBaseError: If an error occurs while interacting with Redis.
        """
        try:
            await self._redis.delete(key)
        except RedisError as e:
            raise CacheBaseError(f"Failed to delete cache for key {key}: {e}") from e

    async def clear_all(self) -> None:
        """
        Clears the entire Redis database.

        Note:
            Use this method with caution as it will remove all keys in the database.

        Raises:
            CacheBaseError: If an error occurs while interacting with Redis.
        """
        try:
            await self._redis.flushdb()
        except RedisError as e:
            raise CacheBaseError(f"Failed to clear cache: {e}") from e

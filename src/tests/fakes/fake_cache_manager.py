from typing import Optional
import json
from cache import CacheManagerInterface, json_serializer


class FakeCacheManager(CacheManagerInterface):
    """
    A fake implementation of CacheManagerInterface for testing purposes.

    Uses an in-memory dictionary to simulate Redis cache operations.
    """

    def __init__(self):
        """
        Initializes the fake cache manager with an in-memory dictionary.
        """
        self._cache = {}

    async def set(self, key: str, value: dict, expiration: int = 3600) -> None:
        """
        Simulates caching data with an expiration time.

        Args:
            key (str): The key under which the data will be cached.
            value (dict): The data to be cached.
            expiration (int): Time-to-live for the cache key in seconds (not implemented for simplicity).
        """
        self._cache[key] = json.dumps(value, default=json_serializer)

    async def get(self, key: str) -> Optional[dict]:
        """
        Simulates retrieving data from the cache.

        Args:
            key (str): The cache key to retrieve.

        Returns:
            Optional[dict]: The cached data if the key exists, otherwise None.
        """
        data = self._cache.get(key)
        return json.loads(data) if data else None

    async def delete(self, key: str) -> None:
        """
        Simulates deleting a specific cache entry by key.

        Args:
            key (str): The cache key to delete.
        """
        if key in self._cache:
            del self._cache[key]

    async def clear_all(self) -> None:
        """
        Simulates clearing the entire cache.

        Note:
            This will remove all keys from the in-memory cache.
        """
        self._cache.clear()

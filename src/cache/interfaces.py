class CacheManagerInterface:
    """
    Interface for Class to manage cache operations.

    Provides methods for setting, retrieving, deleting, and clearing cache entries.
    """

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
        pass

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
        pass

    async def delete(self, key: str) -> None:
        """
        Deletes a specific cache entry by key.

        Args:
            key (str): The cache key to delete.

        Raises:
            CacheBaseError: If an error occurs while interacting with Redis.
        """
        pass

    async def clear_all(self) -> None:
        """
        Clears the entire Redis database.

        Note:
            Use this method with caution as it will remove all keys in the database.

        Raises:
            CacheBaseError: If an error occurs while interacting with Redis.
        """
        pass

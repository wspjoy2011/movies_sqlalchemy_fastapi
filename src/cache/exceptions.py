class CacheBaseError(Exception):
    """Basic exception for Cache manager."""
    pass


class CacheConnectionError(CacheBaseError):
    """Exception raised when connection to cache server failed."""
    def __init__(self, message="Failed to connect to Cache manager"):
        super().__init__(message)

from dataclasses import dataclass


@dataclass(frozen=True)
class RedisConnectionSettingsDTO:
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int

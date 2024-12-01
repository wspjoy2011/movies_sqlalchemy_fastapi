from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional


class InterfaceAuthManager(ABC):

    @classmethod
    @abstractmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        pass

    @classmethod
    @abstractmethod
    def create_refresh_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        pass

    @classmethod
    @abstractmethod
    def decode_access_token(cls, token: str) -> dict:
        pass

    @classmethod
    @abstractmethod
    def decode_refresh_token(cls, token: str) -> dict:
        pass

    @classmethod
    @abstractmethod
    def verify_refresh_token_or_raise(cls, token: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def verify_access_token_or_raise(cls, token: str) -> None:
        pass

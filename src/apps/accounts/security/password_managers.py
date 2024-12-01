import os
from datetime import datetime, timedelta
from typing import Optional

import jwt

from apps.accounts.exceptions import TokenExpiredError, InvalidTokenError
from apps.accounts.interfaces import InterfaceAuthManager


class JWTAuthManager(InterfaceAuthManager):
    _SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
    _SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
    _ALGORITHM = "HS256"

    @classmethod
    def _create_token(cls, data: dict, secret_key: str, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=cls._ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        return cls._create_token(data, cls._SECRET_KEY_ACCESS, expires_delta or timedelta(minutes=10))

    @classmethod
    def create_refresh_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        return cls._create_token(data, cls._SECRET_KEY_REFRESH, expires_delta or timedelta(minutes=60))

    @classmethod
    def decode_access_token(cls, token: str) -> dict:
        return jwt.decode(token, cls._SECRET_KEY_ACCESS, algorithms=[cls._ALGORITHM])

    @classmethod
    def decode_refresh_token(cls, token: str) -> dict:
        return jwt.decode(token, cls._SECRET_KEY_REFRESH, algorithms=[cls._ALGORITHM])

    @classmethod
    def verify_refresh_token_or_raise(cls, token: str) -> None:
        try:
            cls.decode_refresh_token(token)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError
        except jwt.DecodeError:
            raise InvalidTokenError

    @classmethod
    def verify_access_token_or_raise(cls, token: str) -> None:
        try:
            cls.decode_access_token(token)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError
        except jwt.DecodeError:
            raise InvalidTokenError

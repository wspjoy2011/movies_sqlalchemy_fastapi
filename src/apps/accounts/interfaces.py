from abc import ABC, abstractmethod
from datetime import timedelta, datetime, date
from typing import Optional, Tuple

from apps.accounts.dto import (
    UserProfileDTO,
    UserProfileCreateDTO
)
from apps.accounts.schemas import (
    UserResponseSerializer,
    UserCreateSerializer,
    TokenPairRequestSerializer,
    TokenPairResponseSerializer,
    TokenAccessRequestSerializer,
    TokenAccessResponseSerializer
)


class InterfaceUserRepository(ABC):
    @abstractmethod
    async def is_username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    async def is_email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def is_user_id_exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def create_user(self, user: UserCreateSerializer) -> UserResponseSerializer:
        pass

    @abstractmethod
    async def is_user_active(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def set_user_active(self, user_id: int) -> UserResponseSerializer:
        pass

    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponseSerializer]:
        pass


class InterfaceUserProfileRepository(ABC):
    @abstractmethod
    async def is_user_has_profile(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def create_user_profile(self, user_id: int, gender: str, date_of_birth: date, info: str, filename: str
                                  ) -> UserProfileDTO:
        pass


class InterfaceActivationTokenRepository(ABC):
    @abstractmethod
    async def create_token(self, user_id: int, token: str) -> str:
        pass

    @abstractmethod
    async def get_token_data(self, token: str) -> Optional[Tuple[int, datetime]]:
        pass

    @abstractmethod
    async def delete_token(self, token: str) -> None:
        pass


class InterfaceEmailSender(ABC):

    @abstractmethod
    async def send_activation_email(self, email: str, activation_link: str, fullname: str) -> None:
        pass


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


class InterfaceAccountsServices(ABC):
    @abstractmethod
    async def create_user(self, user: UserCreateSerializer, base_url: str) -> UserResponseSerializer:
        pass

    @abstractmethod
    async def activate_user(self, token: str) -> UserResponseSerializer:
        pass

    @abstractmethod
    async def create_user_profile(self, user_profile: UserProfileCreateDTO) -> UserProfileDTO:
        pass


class InterfaceAuthService(ABC):
    @abstractmethod
    async def login(self, login_data: TokenPairRequestSerializer) -> TokenPairResponseSerializer:
        pass

    @abstractmethod
    async def refresh_access_token(self, refresh: TokenAccessRequestSerializer) -> TokenAccessResponseSerializer:
        pass

    @abstractmethod
    async def get_user_id(self, token: str) -> int:
        pass

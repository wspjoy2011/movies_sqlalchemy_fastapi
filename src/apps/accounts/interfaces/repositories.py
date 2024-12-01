from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional, Tuple

from apps.accounts.dto import UserProfileDTO
from apps.accounts.schemas import (
    UserCreateRequestSchema,
    UserResponseSchema
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
    async def create_user(self, user: UserCreateRequestSchema) -> UserResponseSchema:
        pass

    @abstractmethod
    async def is_user_active(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def set_user_active(self, user_id: int) -> UserResponseSchema:
        pass

    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponseSchema]:
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

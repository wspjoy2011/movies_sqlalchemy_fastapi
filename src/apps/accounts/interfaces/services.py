from abc import ABC, abstractmethod

from apps.accounts.dto import (
    UserProfileCreateDTO,
    UserProfileDTO
)
from apps.accounts.schemas import (
    UserCreateRequestSchema,
    UserResponseSchema,
    TokenPairRequestSchema,
    TokenPairResponseSchema,
    TokenAccessRequestSchema,
    TokenAccessResponseSchema
)


class InterfaceAccountsService(ABC):
    @abstractmethod
    async def create_user(self, user: UserCreateRequestSchema, base_url: str) -> UserResponseSchema:
        pass

    @abstractmethod
    async def activate_user(self, token: str) -> UserResponseSchema:
        pass

    @abstractmethod
    async def create_user_profile(self, user_profile: UserProfileCreateDTO) -> UserProfileDTO:
        pass


class InterfaceAuthService(ABC):
    @abstractmethod
    async def login(self, login_data: TokenPairRequestSchema) -> TokenPairResponseSchema:
        pass

    @abstractmethod
    async def refresh_access_token(self, refresh: TokenAccessRequestSchema) -> TokenAccessResponseSchema:
        pass

    @abstractmethod
    async def get_user_id(self, token: str) -> int:
        pass

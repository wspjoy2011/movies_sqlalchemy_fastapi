import secrets
from datetime import datetime, timedelta, timezone

from apps.accounts.dto import UserProfileCreateDTO, UserProfileDTO
from apps.accounts.exceptions import (
    UserAlreadyExists,
    ActivationError,
    InvalidCredentialsError, UserProfileAlreadyExists
)
from apps.accounts.interfaces import (
    InterfaceAuthManager,
    InterfaceAccountsServices,
    InterfaceAuthService, InterfaceUserProfileRepository
)
from apps.accounts.repositories import (
    InterfaceUserRepository,
    InterfaceActivationTokenRepository
)
from apps.accounts.notifications import InterfaceEmailSender
from apps.accounts.schemas import (
    UserCreateSerializer,
    UserResponseSerializer,
    TokenPairRequestSerializer,
    TokenPairResponseSerializer,
    TokenAccessRequestSerializer,
    TokenAccessResponseSerializer
)
from apps.accounts.handlers.interfaces import InterfaceAvatarFileHandler


class AccountsServices(InterfaceAccountsServices):
    def __init__(self,
                 repo_user: InterfaceUserRepository,
                 repo_profile: InterfaceUserProfileRepository,
                 repo_activation_token: InterfaceActivationTokenRepository,
                 email_sender: InterfaceEmailSender,
                 file_handler: InterfaceAvatarFileHandler):
        self._repo_user = repo_user
        self._repo_profile = repo_profile
        self._repo_activation_token = repo_activation_token
        self._email_sender = email_sender
        self._file_handler = file_handler

    async def create_user(self, user: UserCreateSerializer, base_url: str) -> UserResponseSerializer:
        if await self._repo_user.is_username_exists(user.username):
            raise UserAlreadyExists("Username already exists")

        if await self._repo_user.is_email_exists(str(user.email)):
            raise UserAlreadyExists("Email already exists")

        user = await self._repo_user.create_user(user)

        token = secrets.token_hex(16)
        await self._repo_activation_token.create_token(user_id=user.id, token=token)

        fullname = f'{user.first_name.capitalize()} {user.last_name.capitalize()}'
        activation_link = f"{base_url}api/v1/accounts/users/activate/{token}/"
        await self._email_sender.send_activation_email(user.email, activation_link, fullname)

        return user

    async def activate_user(self, token: str) -> UserResponseSerializer:
        token_data = await self._repo_activation_token.get_token_data(token)
        if not token_data:
            raise ActivationError("Invalid activation token")

        user_id, token_created = token_data
        if await self._is_token_expired(token_created):
            await self._repo_activation_token.delete_token(token)
            raise ActivationError("Token has expired")

        is_active = await self._repo_user.is_user_active(user_id)
        if is_active:
            await self._repo_activation_token.delete_token(token)
            raise ActivationError("User already activated")

        user = await self._repo_user.set_user_active(user_id)
        await self._repo_activation_token.delete_token(token)

        return user

    async def create_user_profile(self, user_profile: UserProfileCreateDTO) -> UserProfileDTO:
        user_has_profile = await self._repo_profile.is_user_has_profile(user_profile.user_id)
        if user_has_profile:
            raise UserProfileAlreadyExists

        filename = self._file_handler.save_file(
            filename=user_profile.avatar_filename,
            content=user_profile.avatar_content)
        user_profile_dto = await self._repo_profile.create_user_profile(
            user_id=user_profile.user_id,
            gender=user_profile.gender,
            date_of_birth=user_profile.date_of_birth,
            info=user_profile.info,
            filename=filename
        )
        return user_profile_dto

    async def _is_token_expired(self, token_created: datetime) -> bool:
        now = datetime.now(timezone.utc)
        difference = now - token_created
        return difference > timedelta(days=1)


class AuthService(InterfaceAuthService):
    def __init__(
            self,
            repo_user: InterfaceUserRepository,
            auth_manager: InterfaceAuthManager
    ):
        self._repo_user = repo_user
        self._auth_manager = auth_manager

    async def login(self, login_data: TokenPairRequestSerializer) -> TokenPairResponseSerializer:
        user = await self._repo_user.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise InvalidCredentialsError
        access_token = self._auth_manager.create_access_token(
            data={"user_id": user.id}
        )
        refresh_token = self._auth_manager.create_refresh_token(
            data={"user_id": user.id}
        )
        return TokenPairResponseSerializer(refresh_token=refresh_token, access_token=access_token)

    async def refresh_access_token(self, refresh: TokenAccessRequestSerializer) -> TokenAccessResponseSerializer:
        self._auth_manager.verify_refresh_token_or_raise(refresh.refresh_token)

        refresh_token_data = self._auth_manager.decode_refresh_token(refresh.refresh_token)
        access_token = self._auth_manager.create_access_token(data={"user_id": refresh_token_data["user_id"]})
        return TokenAccessResponseSerializer(access_token=access_token)

    async def get_user_id(self, token: str) -> int:
        self._auth_manager.verify_access_token_or_raise(token)

        access_token_data = self._auth_manager.decode_access_token(token)
        user_id = access_token_data["user_id"]

        is_user_exists = await self._repo_user.is_user_id_exists(user_id)
        if is_user_exists is None:
            raise InvalidCredentialsError

        return user_id

import secrets
from datetime import datetime, timedelta, timezone

from apps.accounts.dto import (
    UserProfileCreateDTO,
    UserProfileDTO
)
from apps.accounts.exceptions import (
    UserAlreadyExists,
    ActivationError,
    UserProfileAlreadyExists
)
from apps.accounts.interfaces import (
    InterfaceAccountsService,
    InterfaceUserRepository,
    InterfaceUserProfileRepository,
    InterfaceActivationTokenRepository,
    InterfaceEmailSender,
    InterfaceAvatarFileHandler,
)
from apps.accounts.schemas import (
    UserCreateRequestSchema,
    UserResponseSchema,
)


class AccountsService(InterfaceAccountsService):
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

    async def create_user(self, user: UserCreateRequestSchema, base_url: str) -> UserResponseSchema:
        if await self._repo_user.is_username_exists(user.username):
            raise UserAlreadyExists("Username already exists")

        if await self._repo_user.is_email_exists(str(user.email)):
            raise UserAlreadyExists("Email already exists")

        user = await self._repo_user.create_user(user)

        token = secrets.token_hex(16)
        await self._repo_activation_token.create_token(user_id=user.id, token=token)

        fullname = f'{user.first_name.capitalize()} {user.last_name.capitalize()}'
        activation_link = f"{base_url}api/v1/accounts/users/activate/{token}/"
        await self._email_sender.send_activation_email(str(user.email), activation_link, fullname)

        return user

    async def activate_user(self, token: str) -> UserResponseSchema:
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

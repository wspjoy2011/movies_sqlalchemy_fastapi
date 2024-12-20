from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.accounts.handlers.files import AvatarFileHandler
from apps.accounts.interfaces import (
    InterfaceUserRepository,
    InterfaceUserProfileRepository,
    InterfaceActivationTokenRepository,
    InterfaceEmailSender,
    InterfaceAuthManager,
    InterfaceAvatarFileHandler,
    InterfaceAccountsService,
    InterfaceAuthService
)
from apps.accounts.repositories import (
    ActivationTokenRepository,
    UserRepository,
    UserProfileRepository
)
from apps.accounts.notifications import EmailSenderGmail
from apps.accounts.security.password_managers import JWTAuthManager
from apps.accounts.services import (
    AuthService,
    AccountsService
)
from apps.accounts.email_templates import REGISTRATION_HTML_CONTENT
from database.session import get_session as get_db
from config.dependencies import get_settings, Settings



async def get_user_repository(
        db: AsyncSession = Depends(get_db)
) -> InterfaceUserRepository:
    return UserRepository(db)


async def get_user_profile_repository(
        db: AsyncSession = Depends(get_db)
) -> InterfaceUserProfileRepository:
    return UserProfileRepository(db)


async def get_activation_token_repository(
        db: AsyncSession = Depends(get_db)
) -> InterfaceActivationTokenRepository:
    return ActivationTokenRepository(db)


async def get_email_sender(
    settings: Settings = Depends(get_settings)
) -> InterfaceEmailSender:
    return EmailSenderGmail(
        hostname=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        email=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        activation_template=REGISTRATION_HTML_CONTENT
    )


async def get_auth_manager() -> InterfaceAuthManager:
    return JWTAuthManager()


async def get_avatar_file_handler(
        settings: Settings = Depends(get_settings)
) -> InterfaceAvatarFileHandler:
    return AvatarFileHandler(media_profile_dir=settings.MEDIA_PROFILE_DIR)


async def get_accounts_service(
        repo_user: InterfaceUserRepository = Depends(get_user_repository),
        repo_profile: InterfaceUserProfileRepository = Depends(get_user_profile_repository),
        repo_activate_token: InterfaceActivationTokenRepository = Depends(get_activation_token_repository),
        email_sender: InterfaceEmailSender = Depends(get_email_sender),
        avatar_file_handler: InterfaceAvatarFileHandler = Depends(get_avatar_file_handler)
) -> InterfaceAccountsService:
    return AccountsService(
        repo_user=repo_user,
        repo_profile=repo_profile,
        repo_activation_token=repo_activate_token,
        email_sender=email_sender,
        file_handler=avatar_file_handler)


async def get_auth_service(
        repo_user: InterfaceUserRepository = Depends(get_user_repository),
        auth_manager: InterfaceAuthManager = Depends(get_auth_manager)
) -> InterfaceAuthService:
    return AuthService(
        repo_user=repo_user,
        auth_manager=auth_manager)

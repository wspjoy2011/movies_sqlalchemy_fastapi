from apps.accounts.exceptions import InvalidCredentialsError
from apps.accounts.interfaces import (
    InterfaceUserRepository,
    InterfaceAuthService,
    InterfaceAuthManager
)
from apps.accounts.schemas import (
    TokenPairRequestSchema,
    TokenPairResponseSchema,
    TokenAccessRequestSchema,
    TokenAccessResponseSchema
)


class AuthService(InterfaceAuthService):
    def __init__(
            self,
            repo_user: InterfaceUserRepository,
            auth_manager: InterfaceAuthManager
    ):
        self._repo_user = repo_user
        self._auth_manager = auth_manager

    async def login(self, login_data: TokenPairRequestSchema) -> TokenPairResponseSchema:
        user = await self._repo_user.authenticate_user(str(login_data.email), login_data.password)
        if not user:
            raise InvalidCredentialsError
        access_token = self._auth_manager.create_access_token(
            data={"user_id": user.id}
        )
        refresh_token = self._auth_manager.create_refresh_token(
            data={"user_id": user.id}
        )
        return TokenPairResponseSchema(refresh_token=refresh_token, access_token=access_token)

    async def refresh_access_token(self, refresh: TokenAccessRequestSchema) -> TokenAccessResponseSchema:
        self._auth_manager.verify_refresh_token_or_raise(refresh.refresh_token)

        refresh_token_data = self._auth_manager.decode_refresh_token(refresh.refresh_token)
        access_token = self._auth_manager.create_access_token(data={"user_id": refresh_token_data["user_id"]})
        return TokenAccessResponseSchema(access_token=access_token)

    async def get_user_id(self, token: str) -> int:
        self._auth_manager.verify_access_token_or_raise(token)

        access_token_data = self._auth_manager.decode_access_token(token)
        user_id = access_token_data["user_id"]

        is_user_exists = await self._repo_user.is_user_id_exists(user_id)
        if is_user_exists is None:
            raise InvalidCredentialsError

        return user_id

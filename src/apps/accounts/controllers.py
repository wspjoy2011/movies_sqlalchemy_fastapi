from fastapi import Depends, HTTPException, Request, status

from apps.accounts.dependencies import get_accounts_service, get_auth_service
from apps.accounts.dto import UserProfileCreateDTO
from apps.accounts.exceptions import UserAlreadyExists, ActivationError, InvalidCredentialsError, TokenExpiredError, \
    InvalidTokenError, UserProfileAlreadyExists
from apps.accounts.interfaces import InterfaceAccountsServices, InterfaceAuthService
from apps.accounts.schemas import UserCreateSerializer, ProfileCreateSerializer, TokenPairRequestSerializer, \
    TokenAccessRequestSerializer, TokenPairResponseSerializer, ProfileResponseSerializer


def get_token(request: Request):
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header missing')
    token = authorization.replace('Bearer ', '')
    return token


async def create_user_controller(
        user: UserCreateSerializer,
        request: Request,
        service: InterfaceAccountsServices = Depends(get_accounts_service)
):
    base_url = str(request.base_url)
    try:
        new_user = await service.create_user(user, base_url)
    except UserAlreadyExists as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exception))
    return {
        "user": new_user,
        "message": f"Check {new_user.email} email for activation link"
    }


async def activate_user_controller(
        token: str,
        service: InterfaceAccountsServices = Depends(get_accounts_service)
):
    try:
        user = await service.activate_user(token)
    except ActivationError as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exception))
    return {
        "user": user,
        "message": "Account successfully activated"
    }


async def create_profile_controller(
        user_id: int,
        token: str = Depends(get_token),
        service_auth: InterfaceAuthService = Depends(get_auth_service),
        service_accounts: InterfaceAccountsServices = Depends(get_accounts_service),
        profile_data: ProfileCreateSerializer = Depends(ProfileCreateSerializer.from_form)
):
    try:
        token_user_id = await service_auth.get_user_id(token)
    except (TokenExpiredError, InvalidTokenError) as exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception))

    if user_id != token_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have access to edit this profile")

    profile_dto = UserProfileCreateDTO(
        user_id=user_id,
        gender=profile_data.gender,
        date_of_birth=profile_data.date_of_birth,
        info=profile_data.info,
        avatar_filename=profile_data.avatar.filename,
        avatar_content=await profile_data.avatar.read()
    )
    try:
        user_profile_dto = await service_accounts.create_user_profile(profile_dto)
    except UserProfileAlreadyExists as exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exception))
    response_profile = ProfileResponseSerializer(**user_profile_dto._asdict())
    return response_profile


async def login_controller(
        login_data: TokenPairRequestSerializer,
        service: InterfaceAuthService = Depends(get_auth_service)
) -> TokenPairResponseSerializer:
    try:
        token_pair = await service.login(login_data)
    except InvalidCredentialsError as exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception))
    return token_pair


async def access_token_refresh_controller(
        refresh_token: TokenAccessRequestSerializer,
        service: InterfaceAuthService = Depends(get_auth_service)
):
    try:
        access_token = await service.refresh_access_token(refresh_token)
    except (TokenExpiredError, InvalidTokenError) as exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception))
    return access_token

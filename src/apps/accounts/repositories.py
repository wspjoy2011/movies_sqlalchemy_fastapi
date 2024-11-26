from datetime import datetime, date
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.accounts.dto import UserProfileDTO
from apps.accounts.interfaces import (
    InterfaceUserRepository,
    InterfaceActivationTokenRepository,
    InterfaceUserProfileRepository
)
from database.models.accounts import (
    User,
    ActivationToken,
    Profile
)
from apps.accounts.schemas import (
    UserCreateSerializer,
    UserResponseSerializer
)
from database.utils import object_as_dict


class UserRepository(InterfaceUserRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_username_exists(self, username: str) -> bool:
        result = await self.db.execute(select(User).filter_by(username=username))
        return result.scalar_one_or_none() is not None

    async def is_email_exists(self, email: str) -> bool:
        result = await self.db.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none() is not None

    async def is_user_id_exists(self, user_id: int) -> bool:
        result = await self.db.execute(select(User).filter_by(id=user_id))
        return result.scalar_one_or_none() is not None

    async def create_user(self, user: UserCreateSerializer) -> UserResponseSerializer:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return UserResponseSerializer(**object_as_dict(db_user))

    async def is_user_active(self, user_id: int) -> bool:
        result = await self.db.execute(select(User.is_active).filter_by(id=user_id))
        is_active_status = result.scalar_one_or_none()
        return is_active_status

    async def set_user_active(self, user_id: int) -> UserResponseSerializer:
        result = await self.db.execute(select(User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        user.is_active = True

        await self.db.commit()
        await self.db.refresh(user)

        return UserResponseSerializer(**object_as_dict(user))

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponseSerializer]:
        result = await self.db.execute(select(User).filter_by(email=email))
        user = result.scalar_one_or_none()

        if user and user.check_password(password):
            return UserResponseSerializer(**object_as_dict(user))

        return None


class UserProfileRepository(InterfaceUserProfileRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_user_has_profile(self, user_id: int) -> bool:
        result = await self.db.execute(select(Profile).filter_by(user_id=user_id))
        return result.scalar_one_or_none() is not None

    async def create_user_profile(
            self,
            user_id: int,
            gender: str,
            date_of_birth:
            date, info: str,
            filename: str
    ) -> UserProfileDTO:
        db_user_profile = Profile(
            user_id=user_id,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=filename
        )
        self.db.add(db_user_profile)
        await self.db.commit()
        await self.db.refresh(db_user_profile)
        return self._map_model_to_dto(db_user_profile)

    def _map_model_to_dto(self, profile: Profile) -> UserProfileDTO:
        profile_dto = UserProfileDTO(
            id=profile.id,
            user_id=profile.user_id,
            gender=profile.gender,
            date_of_birth=profile.date_of_birth,
            info=profile.info,
            avatar=profile.avatar
        )
        return profile_dto


class ActivationTokenRepository(InterfaceActivationTokenRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_token(self, user_id: int, token: str) -> str:
        activation_token = ActivationToken(user_id=user_id, token=token)
        self.db.add(activation_token)
        await self.db.commit()
        await self.db.refresh(activation_token)
        return activation_token.token

    async def get_token_data(self, token: str) -> Optional[Tuple[int, datetime]]:
        result = await self.db.execute(select(ActivationToken).filter_by(token=token))
        activation_token = result.scalar_one_or_none()
        if not activation_token:
            return None
        return activation_token.user_id, activation_token.created

    async def delete_token(self, token: str) -> None:
        result = await self.db.execute(select(ActivationToken).filter_by(token=token))
        activation_token = result.scalar_one_or_none()
        await self.db.delete(activation_token)
        await self.db.commit()

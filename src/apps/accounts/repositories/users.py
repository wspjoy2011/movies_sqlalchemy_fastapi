from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.accounts.interfaces import InterfaceUserRepository
from database.models.accounts import User
from apps.accounts.schemas import (
    UserCreateRequestSchema,
    UserResponseSchema
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

    async def create_user(self, user: UserCreateRequestSchema) -> UserResponseSchema:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return UserResponseSchema(**object_as_dict(db_user))

    async def is_user_active(self, user_id: int) -> bool:
        result = await self.db.execute(select(User.is_active).filter_by(id=user_id))
        is_active_status = result.scalar_one_or_none()
        return is_active_status

    async def set_user_active(self, user_id: int) -> UserResponseSchema:
        result = await self.db.execute(select(User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        user.is_active = True

        await self.db.commit()
        await self.db.refresh(user)

        return UserResponseSchema(**object_as_dict(user))

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponseSchema]:
        result = await self.db.execute(select(User).filter_by(email=email))
        user = result.scalar_one_or_none()

        if user and user.check_password(password):
            return UserResponseSchema(**object_as_dict(user))

        return None
from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.accounts.interfaces import InterfaceActivationTokenRepository
from database.models.accounts import ActivationToken


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

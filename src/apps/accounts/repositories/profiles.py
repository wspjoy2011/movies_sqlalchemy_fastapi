from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.accounts.dto import UserProfileDTO
from apps.accounts.interfaces import InterfaceUserProfileRepository
from database.models.accounts import Profile


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

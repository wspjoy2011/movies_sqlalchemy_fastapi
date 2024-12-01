from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.movies import Genre
from database.utils import object_as_dict
from apps.movies.dto.genre import GenreDTO


class GenreRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_genre(self, name: str) -> GenreDTO:
        genre = Genre(name=name)
        self._session.add(genre)
        await self._session.flush()
        await self._session.refresh(genre)
        return GenreDTO(**object_as_dict(genre))

    async def get_genre(self, genre_id: int) -> Optional[GenreDTO]:
        result = await self._session.execute(select(Genre).filter(Genre.id == genre_id))
        genre = result.scalars().first()
        return GenreDTO(**object_as_dict(genre)) if genre else None

    async def get_all_genres(self) -> List[GenreDTO]:
        result = await self._session.execute(select(Genre))
        genres = result.scalars().all()
        return [GenreDTO(**object_as_dict(genre)) for genre in genres]

    async def update_genre(self, genre_id: int, new_name: str) -> Optional[GenreDTO]:
        result = await self._session.execute(select(Genre).filter(Genre.id == genre_id))
        genre = result.scalars().first()
        if genre:
            genre.name = new_name
            await self._session.flush()
            await self._session.refresh(genre)
            return GenreDTO(**object_as_dict(genre))
        return None

    async def delete_genre(self, genre_id: int) -> bool:
        result = await self._session.execute(select(Genre).filter(Genre.id == genre_id))
        genre = result.scalars().first()
        if genre:
            await self._session.delete(genre)
            await self._session.commit()
            return True
        return False

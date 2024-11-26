import asyncio
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.movies import Genre
from database.session import get_session
from database.utils import object_as_dict
from dto.genre import GenreDTO


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



async def main():
    async with get_session() as session:
        genre_repo = GenreRepository(session)

        new_genre = await genre_repo.create_genre("Drama new")
        print('#' * 10)
        print("Created genre:", new_genre)
        print('#' * 10)

        genre = await genre_repo.get_genre(new_genre.id)
        print('#' * 10)
        print("Fetched genre:", genre)
        print('#' * 10)

        updated_genre = await genre_repo.update_genre(new_genre.id, "Romantic Drama")
        print('#' * 10)
        print("Updated genre:", updated_genre)
        print('#' * 10)

        success = await genre_repo.delete_genre(new_genre.id)
        print('#' * 10)
        print("Deleted genre:", "Success" if success else "Genre not found")
        print('#' * 10)

if __name__ == '__main__':
    asyncio.run(main())

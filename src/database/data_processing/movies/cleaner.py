import asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from database.models.movies import Movie, Genre, Director, Star, Certification, MovieGenre, MovieDirector, MovieStar
from database.session import get_session


class MovieDatabaseCleaner:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def clean_all_movie_data(self):
        try:
            await self._session.execute(delete(MovieGenre))
            await self._session.execute(delete(MovieDirector))
            await self._session.execute(delete(MovieStar))
            await self._session.execute(delete(Movie))
            await self._session.execute(delete(Genre))
            await self._session.execute(delete(Director))
            await self._session.execute(delete(Star))
            await self._session.execute(delete(Certification))

            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            print(f"Error occurred: {e}")
            raise


async def main():
    async with get_session() as session:
        cleaner = MovieDatabaseCleaner(session)
        await cleaner.clean_all_movie_data()


if __name__ == '__main__':
    asyncio.run(main())

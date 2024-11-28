import asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from database.models.movies import Movie, Genre, Director, Star, Certification, MovieGenre, MovieDirector, MovieStar
from database.session import get_session


class MovieDatabaseCleaner:
    """
    A class responsible for cleaning all movie-related data from the database.

    Attributes:
        session (AsyncSession): The asynchronous database session used for operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the MovieDatabaseCleaner with a given database session.

        Args:
            session (AsyncSession): The asynchronous database session.
        """
        self._session = session

    async def clean_all_movie_data(self):
        """
        Deletes all data from movie-related tables in the database.

        The method performs deletions in the following order to maintain integrity:
        1. Deletes relationships (MovieGenre, MovieDirector, MovieStar).
        2. Deletes movies (Movie).
        3. Deletes related entities (Genre, Director, Star, Certification).

        Ensures that the database is clean and all associated records are removed.

        Raises:
            SQLAlchemyError: If an error occurs during the deletion process.
        """
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
    """
    The main function to clean all movie-related data from the database.

    It creates an instance of MovieDatabaseCleaner and calls the `clean_all_movie_data` method
    to remove all data related to movies, genres, directors, stars, and certifications.
    """
    async with get_session() as session:
        cleaner = MovieDatabaseCleaner(session)
        await cleaner.clean_all_movie_data()


if __name__ == '__main__':
    asyncio.run(main())

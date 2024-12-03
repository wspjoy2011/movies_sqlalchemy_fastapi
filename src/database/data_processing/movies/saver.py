import asyncio

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError, DataError

from config.dependencies import Settings, get_settings
from database.models.movies import Genre, Director, Star, Certification, Movie, MovieGenre, MovieDirector, MovieStar
from database.session import get_session_context
from apps.movies.dto.movie import MoviesDTO
from database.data_processing.mappers.csv_mapper import MovieCSVMapper



class MovieDatabaseSaver:
    """
    A class responsible for saving movie-related data to the database.

    Attributes:
        _session (AsyncSession): The asynchronous database session used for operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the MovieDatabaseSaver with a given database session.

        Args:
            session (AsyncSession): The asynchronous database session.
        """
        self._session = session

    async def is_database_populated(self) -> bool:
        """
        Checks if the database is already populated with data.

        Iterates through key tables (Genre, Director, Star, Certification, Movie) and
        verifies if at least one record exists in any of them.

        Returns:
            bool: True if the database is populated, False otherwise.
        """
        try:
            for model in [Genre, Director, Star, Certification, Movie]:
                query = select(model).limit(1)
                result = await self._session.execute(query)
                if result.scalar() is not None:
                    continue
                return False
            return True
        except SQLAlchemyError as e:
            print(f"Error checking database population: {e}")
            return False

    async def save_movies(self, movies_dto: MoviesDTO):
        """
        Saves movies and related data (genres, directors, stars, certifications) to the database.

        Args:
            movies_dto (MoviesDTO): The data transfer object containing movie information.

        Raises:
            IntegrityError: If there is a database integrity constraint violation.
            OperationalError: If there is an operational error with the database.
            DataError: If there is an error in the data format.
            SQLAlchemyError: For other general SQLAlchemy-related exceptions.
            Exception: For unexpected errors.
        """
        try:
            if self._session.in_transaction():
                print("Rolling back existing transaction.")
                await self._session.rollback()

            async with self._session.begin():
                genre_map = {name: Genre(name=name) for name in movies_dto.genres}
                director_map = {name: Director(name=name) for name in movies_dto.directors}
                star_map = {name: Star(name=name) for name in movies_dto.stars}
                certification_map = {name: Certification(name=name) for name in movies_dto.certifications}

                self._session.add_all(genre_map.values())
                self._session.add_all(director_map.values())
                self._session.add_all(star_map.values())
                self._session.add_all(certification_map.values())
                await self._session.flush()

                for movie_dto in movies_dto.movies:
                    movie = Movie(
                        name=movie_dto.name,
                        year=movie_dto.year,
                        time=movie_dto.time,
                        imdb=movie_dto.imdb,
                        votes=movie_dto.votes,
                        meta_score=movie_dto.meta_score,
                        gross=movie_dto.gross,
                        description=movie_dto.description,
                        certification_id=certification_map[movie_dto.certification].id,
                        price=movie_dto.price
                    )
                    self._session.add(movie)
                    await self._session.flush()

                    for genre_name in movie_dto.genres:
                        movie_genre = MovieGenre(movie_id=movie.id, genre_id=genre_map[genre_name].id)
                        self._session.add(movie_genre)

                    for director_name in movie_dto.directors:
                        movie_director = MovieDirector(movie_id=movie.id, director_id=director_map[director_name].id)
                        self._session.add(movie_director)

                    for star_name in movie_dto.stars:
                        movie_star = MovieStar(movie_id=movie.id, star_id=star_map[star_name].id)
                        self._session.add(movie_star)
        except IntegrityError as e:
            await self._session.rollback()
            print(f"Integrity error: {e.orig}")
            raise
        except OperationalError as e:
            await self._session.rollback()
            print(f"Operational error: {e.orig}")
            raise
        except DataError as e:
            await self._session.rollback()
            print(f"Data error: {e.orig}")
            raise
        except SQLAlchemyError as e:
            await self._session.rollback()
            print(f"General SQLAlchemy error: {e}")
            raise
        except Exception as e:
            await self._session.rollback()
            print(f"Unexpected error: {e}")
            raise


async def main(
    settings: Settings = Depends(get_settings),
) -> None:
    """
    The main function to populate the database with movie data.

    It reads data from a CSV file, maps it to a DTO, and saves it to the database.
    Before saving, it checks if the database is already populated to avoid duplication.
    """
    async with get_session_context() as session:
        saver = MovieDatabaseSaver(session)
        if await saver.is_database_populated():
            print("Database is already populated. Skipping data insertion.")
        else:
            print("Database is empty. Populating with data...")
            mapper = MovieCSVMapper(settings.PATH_TO_MOVIES_CSV_FILE)
            movies_dto = mapper.read_csv_and_map_to_dto()
            await saver.save_movies(movies_dto)


if __name__ == '__main__':
    asyncio.run(main())

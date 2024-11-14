import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, SQLAlchemyError

from config.settings import PATH_TO_MOVIES_CSV_FILE
from database.models.movies import Genre, Director, Star, Certification, Movie, MovieGenre, MovieDirector, MovieStar
from database.session import get_session
from dto.movie import MoviesDTO
from mappers.csv_mapper import MovieCSVMapper


class MovieDatabaseSaver:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_movies(self, movies_dto: MoviesDTO):
        try:
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
                        certification_id=certification_map[movie_dto.certification].id
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


async def main():
    mapper = MovieCSVMapper(PATH_TO_MOVIES_CSV_FILE)
    movies_dto = mapper.read_csv_and_map_to_dto()

    async with get_session() as session:
        saver = MovieDatabaseSaver(session)
        await saver.save_movies(movies_dto)


if __name__ == '__main__':
    asyncio.run(main())


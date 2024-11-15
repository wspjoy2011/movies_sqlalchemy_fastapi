import asyncio
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.exceptions.movies import CreateMovieError
from database.models.movies import Movie, Certification
from database.session import get_session
from dto.movie import MovieEntity, MovieDTO, CertificationEntity
from database.utils import object_as_dict


class MovieRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_movie(self, movie_dto: MovieDTO) -> MovieEntity:
        try:
            async with self._session.begin():
                certification_entity = await self._get_or_create_certification_id(movie_dto.certification)
                movie = Movie(
                    name=movie_dto.name,
                    year=movie_dto.year,
                    time=movie_dto.time,
                    imdb=movie_dto.imdb,
                    votes=movie_dto.votes,
                    meta_score=movie_dto.meta_score,
                    gross=movie_dto.gross,
                    description=movie_dto.description,
                    certification_id=certification_entity.id
                )

                self._session.add(movie)
                await self._session.flush()
                await self._session.refresh(movie)
        except SQLAlchemyError as e:
            await self._session.rollback()
            print(f"General SQLAlchemy error: {e}")
            raise CreateMovieError(str(e))
        return MovieEntity(**object_as_dict(movie))

    async def get_movie_by_id(self, movie_id: int) -> Optional[MovieEntity]:
        result = await self._session.execute(select(Movie).filter(Movie.id == movie_id))
        movie = result.scalars().first()
        return MovieEntity(**object_as_dict(movie)) if movie else None

    async def get_all_movies(self) -> List[MovieEntity]:
        result = await self._session.execute(select(Movie))
        movies = result.scalars().all()
        return [MovieEntity(**object_as_dict(movie)) for movie in movies]

    async def _get_or_create_certification_id(self, certification_name: str) -> CertificationEntity:
        result = await self._session.execute(select(Certification).filter_by(name=certification_name))
        certification = result.scalars().first()
        if certification:
            return CertificationEntity(**object_as_dict(certification))

        new_certification = Certification(name=certification_name)
        self._session.add(new_certification)
        await self._session.flush()
        await self._session.refresh(new_certification)
        return CertificationEntity(**object_as_dict(new_certification))


async def main():
    movie_data = MovieDTO(
        name="The Great Adventure",
        year=2023,
        time=120,
        imdb=9.5,
        votes=35,
        meta_score=76.0,
        gross=1200000.0,
        genres={"Adventure", "Drama"},
        certification="PG-13",
        directors={"Jane Doe", "John Smith"},
        stars={"Alice Johnson", "Bob Brown", "Charlie White"},
        description="A thrilling story of a group of friends who set out on a journey to uncover hidden secrets."
    )

    async with get_session() as local_session:
        movie_repo = MovieRepository(local_session)
        new_movie_entity = await movie_repo.create_movie(movie_data)
        print(new_movie_entity)


if __name__ == '__main__':
    asyncio.run(main())

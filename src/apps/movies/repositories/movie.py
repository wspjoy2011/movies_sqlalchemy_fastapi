from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.exceptions.movies import CreateMovieError
from database.models.movies import Movie, Certification
from database.session import get_session
from apps.movies.dto.movie import MovieEntity, MovieDTO, CertificationEntity
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
                    certification_id=certification_entity.id,
                    price=movie_dto.price
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

    async def get_movies_with_pagination(self, offset: int, limit: int) -> list[MovieEntity]:
        """
        Retrieve movies with pagination.

        Args:
            offset (int): The offset for the query.
            limit (int): The maximum number of items to retrieve.

        Returns:
            list[MovieEntity]: A list of paginated movies.
        """
        result = await self._session.execute(
            select(Movie).offset(offset).limit(limit)
        )
        movies = result.scalars().all()
        return [MovieEntity(**object_as_dict(movie)) for movie in movies]

    async def get_total_count(self) -> int:
        """
        Retrieve the total count of movies in the database.

        Returns:
            int: The total count of movies.
        """
        result = await self._session.execute(select(func.count(Movie.id)))
        return result.scalar()

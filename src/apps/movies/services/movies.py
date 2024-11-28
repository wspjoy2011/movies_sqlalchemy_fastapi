from typing import List

from apps.movies.dto.movie import MovieEntity
from apps.movies.repositories.movie import MovieRepository
from apps.movies.schemas import MovieSchema


class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self._movie_repository = movie_repository

    async def get_all_movies(self) -> List[MovieSchema]:
        movies = await self._movie_repository.get_all_movies()
        return [MovieSchema(**movie.as_dict()) for movie in movies]

    async def get_paginated_movies(self, offset: int, limit: int) -> tuple[List[MovieEntity], int]:
        """
        Retrieve paginated movies and the total count.

        Args:
            offset (int): The offset for the query.
            limit (int): The maximum number of items to retrieve.

        Returns:
            tuple: A list of MovieEntity and the total count of movies.
        """
        movies = await self._movie_repository.get_movies_with_pagination(offset, limit)
        total_count = await self._movie_repository.get_total_count()

        return movies, total_count

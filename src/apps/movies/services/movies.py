from apps.movies import MovieServiceInterface
from apps.movies import MovieRepositoryInterface
from cache import CacheManagerInterface
from apps.movies.schemas import MovieListResponseSchema, MovieResponseSchema


class MovieService(MovieServiceInterface):
    def __init__(
            self,
            movie_repository: MovieRepositoryInterface,
            cache_manager: CacheManagerInterface
    ):
        self._movie_repository = movie_repository
        self._cache_manager = cache_manager

    async def get_paginated_movies(self, page: int, per_page: int) -> MovieListResponseSchema:
        """
        Retrieve paginated movies and the total count, utilizing caching.

        Args:
            page (int): The current page number (1-indexed).
            per_page (int): The number of items per page.

        Returns:
            MovieListResponseSchema: The paginated response schema.
        """
        cache_key = f"movies:page:{page}:per_page:{per_page}"

        cached_response = await self._cache_manager.get(cache_key)
        if cached_response:
            return MovieListResponseSchema(**cached_response)

        offset = (page - 1) * per_page

        movies = await self._movie_repository.get_movies_with_pagination(offset, per_page)
        total_count = await self._movie_repository.get_total_count()

        movies_schema = [MovieResponseSchema(**movie.as_dict()) for movie in movies]
        response = MovieListResponseSchema(movies=movies_schema, total=total_count)

        await self._cache_manager.set(cache_key, response.model_dump())

        return response

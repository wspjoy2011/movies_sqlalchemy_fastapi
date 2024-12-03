from abc import ABC, abstractmethod

from apps.movies.schemas import MovieListResponseSchema


class MovieServiceInterface(ABC):

    @abstractmethod
    async def get_paginated_movies(self, page: int, per_page: int) -> MovieListResponseSchema:
        """
        Retrieve paginated movies and the total count, utilizing caching.

        Args:
            page (int): The current page number (1-indexed).
            per_page (int): The number of items per page.

        Returns:
            MovieListResponseSchema: The paginated response schema.
        """
        pass

from abc import ABC, abstractmethod
from typing import Optional

from apps.movies.dto.movie import MovieDTO, MovieEntity, CertificationEntity


class MovieRepositoryInterface(ABC):

    @abstractmethod
    async def create_movie(self, movie_dto: MovieDTO) -> MovieEntity:
        pass

    @abstractmethod
    async def get_movie_by_id(self, movie_id: int) -> Optional[MovieEntity]:
       pass

    @abstractmethod
    async def get_all_movies(self) -> list[MovieEntity]:
        pass

    @abstractmethod
    async def get_movies_with_pagination(self, offset: int, limit: int) -> list[MovieEntity]:
        """
        Retrieve movies with pagination.

        Args:
            offset (int): The offset for the query.
            limit (int): The maximum number of items to retrieve.

        Returns:
            list[MovieEntity]: A list of paginated movies.
        """
        pass

    @abstractmethod
    async def get_total_count(self) -> int:
        """
        Retrieve the total count of movies in the database.

        Returns:
            int: The total count of movies.
        """
        pass


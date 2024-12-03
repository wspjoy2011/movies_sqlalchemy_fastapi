import uuid
from typing import List, Optional
from apps.movies import MovieRepositoryInterface
from apps.movies.dto.movie import MovieDTO, MovieEntity, CertificationEntity


class FakeMovieRepository(MovieRepositoryInterface):
    """
    A fake implementation of MovieRepositoryInterface for testing purposes.

    Uses in-memory data structures to simulate database operations.
    """

    def __init__(self):
        """
        Initializes the fake repository with in-memory storage.
        """
        self._movies = []  # List to store MovieEntity objects
        self._certifications = {}  # Dictionary to store CertificationEntity by name
        self._next_movie_id = 1  # Auto-incrementing ID for movies
        self._next_certification_id = 1  # Auto-incrementing ID for certifications
        self._calls = {
            "get_movies_with_pagination": 0,
            "get_total_count": 0,
        }

    async def create_movie(self, movie_dto: MovieDTO) -> MovieEntity:
        """
        Simulates creating a movie in the repository.

        Args:
            movie_dto (MovieDTO): The data transfer object containing movie information.

        Returns:
            MovieEntity: The created movie entity.
        """
        certification = await self._get_or_create_certification_id(movie_dto.certification)

        movie = MovieEntity(
            id=self._next_movie_id,
            uuid=uuid.uuid4(),
            name=movie_dto.name,
            year=movie_dto.year,
            time=movie_dto.time,
            imdb=movie_dto.imdb,
            votes=movie_dto.votes,
            meta_score=movie_dto.meta_score,
            gross=movie_dto.gross,
            description=movie_dto.description,
            certification_id=certification.id,
            price=movie_dto.price
        )

        self._movies.append(movie)
        self._next_movie_id += 1
        return movie

    async def get_movie_by_id(self, movie_id: int) -> Optional[MovieEntity]:
        """
        Simulates retrieving a movie by its ID.

        Args:
            movie_id (int): The ID of the movie to retrieve.

        Returns:
            Optional[MovieEntity]: The retrieved movie entity, or None if not found.
        """
        for movie in self._movies:
            if movie.id == movie_id:
                return movie
        return None

    async def get_all_movies(self) -> List[MovieEntity]:
        """
        Simulates retrieving all movies.

        Returns:
            List[MovieEntity]: A list of all movies.
        """
        return self._movies

    async def get_movies_with_pagination(self, offset: int, limit: int) -> list[MovieEntity]:
        """
        Simulates retrieving movies with pagination.

        Args:
            offset (int): The offset for the query.
            limit (int): The maximum number of items to retrieve.

        Returns:
            list[MovieEntity]: A list of paginated movies.
        """
        self._calls["get_movies_with_pagination"] += 1
        return self._movies[offset:offset + limit]

    async def get_total_count(self) -> int:
        """
        Simulates retrieving the total count of movies.

        Returns:
            int: The total count of movies.
        """
        self._calls["get_total_count"] += 1
        return len(self._movies)

    async def _get_or_create_certification_id(self, certification_name: str) -> CertificationEntity:
        """
        Simulates retrieving or creating a certification.

        Args:
            certification_name (str): The name of the certification.

        Returns:
            CertificationEntity: The retrieved or created certification entity.
        """
        if certification_name in self._certifications:
            return self._certifications[certification_name]

        certification = CertificationEntity(
            id=self._next_certification_id,
            name=certification_name
        )
        self._certifications[certification_name] = certification
        self._next_certification_id += 1
        return certification

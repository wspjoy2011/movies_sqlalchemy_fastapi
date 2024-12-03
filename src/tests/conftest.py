from uuid import UUID

import pytest

from apps.movies.dto.movie import MovieEntity
from tests.fakes.fake_movie_repository import FakeMovieRepository
from tests.fakes.fake_cache_manager import FakeCacheManager
from decimal import Decimal

@pytest.fixture
def fake_movie_data():
    """Provide test movie data."""
    return [
        MovieEntity(
            id=1,
            uuid=UUID("3e60b427-6840-4bd9-95c4-a3d840eac227"),
            name="The Shawshank Redemption",
            year=1994,
            time=142,
            imdb=9.3,
            votes=2804443,
            meta_score=82,
            gross=28340000,
            description="Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
            certification_id=18,
            price=Decimal("19.6"),
        )
    ]

@pytest.fixture
def fake_movie_repository(fake_movie_data):
    """Provide a fake movie repository pre-filled with test data."""
    repository = FakeMovieRepository()
    repository._movies.extend(fake_movie_data)
    return repository


@pytest.fixture
def fake_cache_manager():
    """Provide a fake cache manager."""
    return FakeCacheManager()

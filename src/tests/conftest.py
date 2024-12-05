from decimal import Decimal
from uuid import UUID

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from apps.accounts.dependencies import get_accounts_service
from apps.accounts.repositories import UserRepository, ActivationTokenRepository
from apps.accounts.schemas import UserCreateRequestSchema
from apps.accounts.services import AccountsService
from apps.movies.dto.movie import MovieEntity
from database.session_test import setup_sqlite_database, get_sqlite_session_context, reset_sqlite_database
from main import app
from tests.fakes.fake_email_sender import FakeEmailSender
from tests.fakes.fake_movie_repository import FakeMovieRepository
from tests.fakes.fake_cache_manager import FakeCacheManager


@pytest_asyncio.fixture
async def sqlite_session():
    """
    Fixture to provide an SQLite session for each test.
    Ensures the database is set up before use and reset after the test.
    """
    await setup_sqlite_database()

    async with get_sqlite_session_context() as session:
        yield session

    await reset_sqlite_database()


@pytest_asyncio.fixture
async def fake_email_sender():
    """
    Fixture to provide a fake email sender for testing.
    """
    return FakeEmailSender()


@pytest_asyncio.fixture
async def accounts_service(sqlite_session, fake_email_sender):
    """
    Fixture to provide an instance of AccountsService for testing.
    """
    user_repo = UserRepository(db=sqlite_session)
    token_repo = ActivationTokenRepository(db=sqlite_session)

    service = AccountsService(
        repo_user=user_repo,
        repo_profile=None,
        repo_activation_token=token_repo,
        email_sender=fake_email_sender,
        file_handler=None
    )
    return service


@pytest.fixture
def override_accounts_service(accounts_service):
    """
    Substitute `get_accounts service` dependency using `accounts service` fixture.
    """
    app.dependency_overrides[get_accounts_service] = lambda: accounts_service
    yield
    app.dependency_overrides = {}


@pytest.fixture
def test_client():
    """
    Fixture for FastAPI TestClient.
    """
    return TestClient(app)


@pytest.fixture
def user_data():
    """
    Fixture to provide user data for testing.
    """
    return UserCreateRequestSchema(
        username="testuser",
        email="testuser@example.com",
        password="P@ssw0rd",
        first_name="Test",
        last_name="User"
    )


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

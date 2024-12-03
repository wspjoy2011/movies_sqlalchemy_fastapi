import pytest

from apps.movies import MovieService
from apps.movies.schemas import MovieListResponseSchema, MovieResponseSchema
from tests.fakes.fake_movie_repository import FakeMovieRepository


@pytest.mark.asyncio
async def test_get_paginated_movies(fake_movie_repository, fake_cache_manager, fake_movie_data):
    """
    Test the get_paginated_movies method with fake repository and cache,
    and ensure that the returned data matches the expected data.
    """
    service = MovieService(fake_movie_repository, fake_cache_manager)

    response = await service.get_paginated_movies(page=1, per_page=1)

    assert isinstance(response, MovieListResponseSchema)
    assert response.total == len(fake_movie_data)
    assert len(response.movies) == 1

    returned_movie = response.movies[0].model_dump()
    expected_movie = fake_movie_data[0].as_dict()

    assert returned_movie == expected_movie


@pytest.mark.asyncio
async def test_get_paginated_movies_cache(fake_movie_repository, fake_cache_manager, fake_movie_data):
    """
    Test that the get_paginated_movies method stores data in the cache after retrieval.
    """
    service = MovieService(fake_movie_repository, fake_cache_manager)
    page = 1
    per_page = 1
    cache_key = f"movies:page:{page}:per_page:{per_page}"

    assert await fake_cache_manager.get(cache_key) is None

    response = await service.get_paginated_movies(page=page, per_page=per_page)

    assert isinstance(response, MovieListResponseSchema)
    assert response.total == len(fake_movie_data)
    assert len(response.movies) == 1

    returned_movie = response.movies[0].model_dump()
    expected_movie = fake_movie_data[0].as_dict()
    assert returned_movie == expected_movie

    cached_data = await fake_cache_manager.get(cache_key)
    assert cached_data is not None

    cached_response = MovieListResponseSchema(**cached_data)
    assert cached_response.total == len(fake_movie_data)
    assert len(cached_response.movies) == 1

    cached_movie = cached_response.movies[0].model_dump()
    assert cached_movie == expected_movie


@pytest.mark.asyncio
async def test_get_paginated_movies_empty_repository(fake_cache_manager):
    """
    Test get_paginated_movies when the repository is empty.
    """
    fake_repository = FakeMovieRepository()
    service = MovieService(fake_repository, fake_cache_manager)

    response = await service.get_paginated_movies(page=1, per_page=10)

    assert isinstance(response, MovieListResponseSchema)
    assert response.total == 0
    assert len(response.movies) == 0

    cache_key = "movies:page:1:per_page:10"
    cached_data = await fake_cache_manager.get(cache_key)
    assert cached_data == {'movies': [], 'total': 0}


@pytest.mark.asyncio
async def test_get_paginated_movies_cache_hit(fake_movie_repository, fake_cache_manager, fake_movie_data):
    """
    Test that get_paginated_movies retrieves data from the cache if it exists.
    """
    service = MovieService(fake_movie_repository, fake_cache_manager)
    page = 1
    per_page = 1
    cache_key = f"movies:page:{page}:per_page:{per_page}"

    preloaded_response = MovieListResponseSchema(
        movies=[MovieResponseSchema(**fake_movie_data[0].as_dict())],
        total=len(fake_movie_data)
    )
    await fake_cache_manager.set(cache_key, preloaded_response.model_dump())

    response = await service.get_paginated_movies(page=page, per_page=per_page)

    assert response == preloaded_response

    assert fake_movie_repository._calls["get_movies_with_pagination"] == 0
    assert fake_movie_repository._calls["get_total_count"] == 0

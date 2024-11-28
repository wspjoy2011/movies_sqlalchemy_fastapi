import json
from decimal import Decimal
from typing import Any, Union
from uuid import UUID

import aioredis
from fastapi import Query

from apps.movies.repositories.movie import MovieRepository
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from database.session import get_session
from apps.movies.services.movies import MovieService
from apps.movies.schemas import MovieListSchemaResponse, MovieSchema


async def get_redis_connection() -> aioredis.Redis:
    """
    Establish and return a connection to Redis.
    """
    return await aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        password=REDIS_PASSWORD,
        decode_responses=True
    )


def json_serializer(obj: Union[UUID, Decimal]) -> Union[str, float]:
    """
    Custom JSON serializer for unsupported types such as UUID and Decimal.

    Args:
        obj (Union[UUID, Decimal]): The object to serialize. Supports UUID and Decimal types.

    Returns:
        Union[str, float]: A JSON-serializable representation of the object:
            - str for UUID,
            - float for Decimal.

    Raises:
        TypeError: If the object type is not supported for serialization.
    """
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


async def get_all_movies(
    page: int = Query(1, ge=1, description="Page number, must be 1 or greater"),
    per_page: int = Query(10, ge=1, le=20, description="Number of items per page, must be between 1 and 20")
) -> MovieListSchemaResponse:
    """
    Endpoint to retrieve all movies with pagination, with Redis caching.

    Args:
        page (int): Page number, defaults to 1.
        per_page (int): Number of items per page, defaults to 10. Must be between 1 and 20.

    Returns:
        MovieListSchemaResponse: The paginated list of movies and the total count.
    """
    cache_key = f"movies:page:{page}:per_page:{per_page}"

    redis = await get_redis_connection()

    cached_data = await redis.get(cache_key)
    if cached_data:
        cached_response = json.loads(cached_data)
        return MovieListSchemaResponse(**cached_response)

    async with get_session() as session:
        movie_repository = MovieRepository(session)
        movie_service = MovieService(movie_repository)

        offset = (page - 1) * per_page
        movies, total_count = await movie_service.get_paginated_movies(offset=offset, limit=per_page)
        movies_schema = [MovieSchema(**movie.as_dict()) for movie in movies]

        response = MovieListSchemaResponse(movies=movies_schema, total=total_count)

        await redis.set(
            cache_key,
            json.dumps(response.model_dump(), default=json_serializer),
            ex=3600
        )

        return response

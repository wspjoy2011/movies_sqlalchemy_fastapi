from fastapi import Query, Depends

from apps.movies import MovieServiceInterface
from apps.movies.dependencies import get_movie_service
from apps.movies.schemas import MovieListResponseSchema


async def get_all_movies(
    page: int = Query(1, ge=1, description="Page number, must be 1 or greater"),
    per_page: int = Query(10, ge=1, le=20, description="Number of items per page, must be between 1 and 20"),
    movie_service: MovieServiceInterface = Depends(get_movie_service)
) -> MovieListResponseSchema:
    """
    Endpoint to retrieve all movies with pagination.

    Args:
        page (int): Page number.
        per_page (int): Number of items per page.
        movie_service(MovieServiceInterface): Domain logic

    Returns:
        MovieListResponseSchema: Paginated movies and total count.
    """
    return await movie_service.get_paginated_movies(page=page, per_page=per_page)

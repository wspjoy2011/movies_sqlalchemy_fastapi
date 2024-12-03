from fastapi import Depends

from apps.movies import (
    MovieRepository,
    MovieService,
    MovieRepositoryInterface,
    MovieServiceInterface
)
from cache import CacheManagerInterface
from config.dependencies import get_cache_manager
from database.session import (
    get_session,
    AsyncSession
)


def _get_movie_repository(
    session: AsyncSession = Depends(get_session),
) -> MovieRepositoryInterface:
    return MovieRepository(session=session)



def get_movie_service(
    movie_repository: MovieRepositoryInterface = Depends(_get_movie_repository),
    cache_manager: CacheManagerInterface = Depends(get_cache_manager)
) -> MovieServiceInterface:
    return MovieService(
        movie_repository=movie_repository,
        cache_manager=cache_manager
    )

from fastapi import APIRouter
from apps.movies.controllers import (
    get_all_movies
)

router = APIRouter()

router.get("/movies", status_code=200)(get_all_movies)

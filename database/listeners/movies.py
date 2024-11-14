from sqlalchemy import event

from database.models.movies import Movie
from database.validators.movies import validate_movie_popularity


@event.listens_for(Movie, "before_insert")
@event.listens_for(Movie, "before_update")
def validate_movie_combination_fields(mapper, connection, target):
    validate_movie_popularity(target.imdb, target.votes)

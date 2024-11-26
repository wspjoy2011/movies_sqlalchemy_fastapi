from datetime import datetime
from typing import Optional


def validate_year(value: int) -> int:
    first_film_year = 1888
    current_year = datetime.now().year
    if value < first_film_year or value > current_year + 2:
        raise ValueError(f"The year {value} is invalid. Must be between {first_film_year} and {current_year + 2}.")
    return value


def validate_imdb(value: float) -> float:
    if value < 0.1 or value > 10.0:
        raise ValueError(f"IMDb rating {value} is invalid. Must be between 0.1 and 10.0.")
    return value


def validate_votes(value: int) -> int:
    if value < 0:
        raise ValueError("Votes cannot be negative.")
    return value


def validate_meta_score(value: Optional[float]) -> Optional[float]:
    if value is not None and (value < 0 or value > 100):
        raise ValueError(f"MetaScore {value} is invalid. Must be between 0 and 100.")
    return value


def validate_time(value: int) -> int:
    if value <= 0:
        raise ValueError("Runtime must be positive.")
    return value


def validate_gross(value: Optional[float]) -> Optional[float]:
    if value is not None and value < 0:
        raise ValueError("Gross cannot be negative.")
    return value


def validate_movie_popularity(imdb: float, votes: int) -> None:
    if imdb > 9.0 and votes < 1000:
        raise ValueError("For IMDb ratings above 9.0, votes must be at least 1000.")

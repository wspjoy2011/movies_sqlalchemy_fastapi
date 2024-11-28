from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4
from typing import Optional


@dataclass
class MovieDTO:
    """
    Data transfer object for a Movie.

    Attributes:
        name (str): The name of the movie.
        year (int): The release year of the movie.
        time (int): The runtime of the movie in minutes.
        imdb (float): The IMDb rating of the movie.
        votes (int): The number of votes the movie received.
        meta_score (Optional[float]): The MetaScore rating of the movie.
        gross (Optional[float]): The gross earnings of the movie.
        genres (set[str]): The set of genres associated with the movie.
        certification (str): The certification of the movie (e.g., PG-13).
        directors (set[str]): The set of directors of the movie.
        stars (set[str]): The set of stars/actors in the movie.
        description (str): The description of the movie.
        price (Optional[Decimal]): The price of the movie in a decimal format.
    """
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float]
    gross: Optional[float]
    genres: set[str]
    certification: str
    directors: set[str]
    stars: set[str]
    description: str
    price: Optional[Decimal]


@dataclass
class MoviesDTO:
    genres: set
    certifications: set
    directors: set
    stars: set
    movies: list[MovieDTO]


@dataclass
class MovieEntity:
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float]
    gross: Optional[float]
    description: str
    id: int
    uuid: uuid4
    certification_id: int
    price: Optional[Decimal]

    def as_dict(self) -> dict:
        return vars(self)


@dataclass
class CertificationEntity:
    id: int
    name: str

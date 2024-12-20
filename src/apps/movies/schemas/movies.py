from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class MovieResponseSchema(BaseModel):
    id: int
    uuid: UUID
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    certification_id: int
    price: Optional[Decimal] = None

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieResponseSchema]
    total: int

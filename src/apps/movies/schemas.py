from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class MovieSchema(BaseModel):
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


class MovieListSchemaResponse(BaseModel):
    movies: List[MovieSchema]
    total: int

from pydantic import BaseModel, ValidationError
from typing import Optional, List, Any


class ElasticRequest(BaseModel):
    title: Optional[str]
    year: Optional[int]
    genre: Optional[List[str]]  # <- я хз почему я не сделал множественное число как в возврате, но мне лень пиздец менять
    director: Optional[str]
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class MovieItem(BaseModel):
    movie_id: int
    movie_title: Optional[str]
    year: Optional[int]
    director: Optional[str]
    description: Optional[str]
    info_title: Optional[str]
    genres: Optional[List[str]]
    average_rating: Optional[float]

class MovieInfoResponse(BaseModel):
    movie: MovieItem

class ElasticResponse(BaseModel):
    movies: List[MovieItem]


class MovieInfoResponse(BaseModel):
    movie: MovieItem

class MovieRequest(BaseModel):
    movie_id: int
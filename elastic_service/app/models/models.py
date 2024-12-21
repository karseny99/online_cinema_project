from pydantic import BaseModel, ValidationError, Field
from typing import Optional, List, Any

class ElasticRequest(BaseModel):
    title: Optional[str]
    year: Optional[int]
    genre: Optional[List[Optional[str]]] 
    director: Optional[str]
    page: Optional[int]
    page_size: Optional[int]


class MovieItem(BaseModel):
    movie_id: Optional[int]
    movie_title: Optional[str]
    year: Optional[int]
    director: Optional[str]
    description: Optional[str]
    info_title: Optional[str]
    genres: Optional[List[Optional[str]]]
    average_rating: Optional[float]


class ElasticResponse(BaseModel):
    movies: List[MovieItem]
    success: bool


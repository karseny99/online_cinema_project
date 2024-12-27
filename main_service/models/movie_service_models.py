from pydantic import BaseModel, ValidationError
from typing import Optional, List, Any


class ElasticRequest(BaseModel):
    title: Optional[str]
    year: Optional[int]
    genre: Optional[
    List[Optional[str]]]  
    director: Optional[str]
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class MovieItem(BaseModel):
    movie_id: Optional[int]
    movie_title: Optional[str]
    year: Optional[int]
    director: Optional[str]
    description: Optional[str]
    info_title: Optional[str]
    genres: Optional[List[Optional[str]]]
    average_rating: Optional[float]
    movie_url: Optional[str] = None
    movie_poster_url: Optional[str] = None

class ElasticResponse(BaseModel):
    movies: List[MovieItem]
    success: bool


class MovieInfoResponse(BaseModel):
    movie: Optional[MovieItem]
    success: bool


class MovieRequest(BaseModel):
    movie_id: int


class GenresResponse(BaseModel):
    genres: Optional[List[Optional[str]]]
    success: bool

    
class RecommendationRequest(BaseModel):
    user_id: int


class RecommendationResponse(BaseModel):
    movies: Optional[List[Optional[MovieItem]]]
    success: bool

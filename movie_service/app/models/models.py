from pydantic import BaseModel, ValidationError
from typing import Optional, List, Any
from app.repository.models import MoviesWithInfo

class MovieItem(BaseModel):
    movie_id: int
    movie_title: Optional[str]
    year: Optional[int]
    director: Optional[str]
    description: Optional[str]
    info_title: Optional[str]
    genres: Optional[List[Optional[str]]]
    average_rating: Optional[float]
    movie_url: Optional[str]
    movie_poster_url: Optional[str]

    @classmethod
    def from_orm(cls, movie_orm: MoviesWithInfo) -> "MovieItem":
        return cls(
            movie_id=movie_orm.movie_id,
            movie_title=movie_orm.movie_title,
            year=movie_orm.year,
            director=movie_orm.director,
            description=movie_orm.description,
            info_title=movie_orm.info_title,
            genres=movie_orm.genres,
            average_rating=movie_orm.average_rating,
            movie_url="",
            movie_poster_url="",
        )


class MovieInfoResponse(BaseModel):
    movie: Optional[MovieItem]
    success: bool

class MovieRequest(BaseModel):
    movie_id: int

class GenresResponse(BaseModel):
    genres: Optional[List[Optional[str]]]
    success: bool
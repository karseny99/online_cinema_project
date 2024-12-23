from pydantic import BaseModel
from typing import Any, Optional


class SetMovieRatingRequest(BaseModel):
    movie_id: int
    user_id: int
    rating: float


class SetMovieRatingResponse(BaseModel):
    movie_id: int
    user_id: int
    success: bool
    message: str


class GetMovieRatingRequest(BaseModel):
    movie_id: Optional[int] = None
    user_id: Optional[int] = None


class GetMovieRatingResponse(BaseModel):
    movie_id: Optional[int] = None
    user_id: Optional[int] = None
    rating: Optional[int] = None
    success: bool
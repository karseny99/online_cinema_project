from pydantic import BaseModel
from typing import Any


class SetMovieRatingRequest(BaseModel):
    movie_id: int
    user_id: int
    rating: float


class SetMovieRatingResponse(BaseModel):
    movie_id: int
    user_id: int
    success: bool
    message: str

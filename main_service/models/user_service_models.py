from pydantic import BaseModel

class SetMovieRatingRequest(BaseModel):
    movie_id: int
    user_id: int
    rating: float

class SetMovieRatingResponse(BaseModel):
    movie_id: int
    user_id: int
    success: bool

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
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

class UserInfoRequest(BaseModel):
    user_id: int

class UserInfoResponse(BaseModel):
    user_id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    role: Optional[str]
    registered_at: Optional[datetime]
    success: bool
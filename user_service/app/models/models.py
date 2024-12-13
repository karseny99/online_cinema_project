from pydantic import BaseModel
from typing import Any

class BaseContractModel(BaseModel):
    contract_type: str  # Поле для указания типа контракта "search_request"
    body: Any
    # request_id: str

class SetMovieRatingRequest(BaseModel):
    movie_id: int
    user_id: int
    rating: float

class SetMovieRatingResponse(BaseModel):
    movie_id: int
    user_id: int
    success: bool

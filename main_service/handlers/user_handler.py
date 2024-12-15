from fastapi import APIRouter

from models.user_service_models import SetMovieRatingResponse, SetMovieRatingRequest
from service.user_service import UserService

router = APIRouter()

@router.post("/set-rating", response_model=SetMovieRatingResponse)
def set_movie_rating(req: SetMovieRatingRequest):
    user_service = UserService()
    resp = user_service.set_movie_rating(req)
    return resp

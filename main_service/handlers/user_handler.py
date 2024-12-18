import http
import logging
from fastapi import APIRouter, Response, Depends
from handlers.middleware import get_current_user

from models.user_service_models import SetMovieRatingResponse, SetMovieRatingRequest
from service.user_service import set_rating

router = APIRouter()
log = logging.getLogger(__name__)

@router.post("/set-rating", response_model=SetMovieRatingResponse)
def set_movie_rating(
        req: SetMovieRatingRequest,
        response: Response,
        current_user: dict = Depends(get_current_user)
):

    username = current_user["sub"]
    print(f"Hello, {username}!")
    print(f"Requested user_id: {req.user_id}")

    resp = set_rating(req=req)

    if resp is None:
        response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        return SetMovieRatingResponse(
            movie_id=req.movie_id,
            user_id=req.movie_id,
            message="service is unavailable for now",
            success=False
        )

    response.body = resp
    if resp.success:
        response.status_code = http.HTTPStatus.OK
    else:
        response.status_code = http.HTTPStatus.BAD_REQUEST
    return resp


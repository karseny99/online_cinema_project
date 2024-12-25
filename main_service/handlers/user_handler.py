import http
import logging
from fastapi import APIRouter, Response, Depends
from handlers.middleware import get_current_user

from models.user_service_models import SetMovieRatingResponse, SetMovieRatingRequest, GetMovieRatingRequest, GetMovieRatingResponse, UserRoleRequest, UserRoleResponse
from service.user_service import set_rating, get_rating, get_role

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/set-rating", response_model=SetMovieRatingResponse)
def set_movie_rating(
        req: SetMovieRatingRequest,
        response: Response,
        current_user: dict = Depends(get_current_user)
):
    user_id = current_user["sub"]
    req.user_id = user_id # вытягиваем из токена фактический user_id
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


@router.get("/get-rating", response_model=GetMovieRatingResponse)
def get_movie_rating(
        movie_id: int,
        current_user: dict = Depends(get_current_user)
):
    req = GetMovieRatingRequest(user_id=current_user["sub"], movie_id=movie_id)
    resp = get_rating(req)

    return resp
    

@router.get("/get-role", response_model=UserRoleResponse)
def get_user_role(current_user: dict = Depends(get_current_user)):
    req = UserRoleRequest(user_id=current_user["sub"])
    resp = get_role(req)
    return resp

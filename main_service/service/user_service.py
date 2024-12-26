import logging
import json

from rpc_client.rpc_client import get_user_rpc_client, get_movie_rpc_client
from models.user_service_models import SetMovieRatingRequest, SetMovieRatingResponse, GetMovieRatingRequest, GetMovieRatingResponse, UserInfoRequest, UserInfoResponse
from models.movie_service_models import RecommendationRequest, RecommendationResponse

log = logging.getLogger(__name__)


def set_rating(req: SetMovieRatingRequest) -> SetMovieRatingResponse:
    set_rating_function_name = "set_movie_rating"
    rpc_client = get_user_rpc_client()

    result = str(rpc_client.send_task(set_rating_function_name, req))
    result = json.loads(result)
    result = SetMovieRatingResponse(**result)

    return result

def get_rating(req: GetMovieRatingRequest) -> GetMovieRatingResponse:

    get_rating_function_name = "get_movie_rating"
    
    result = get_user_rpc_client().send_task(get_rating_function_name, req)

    if not result:
        return GetMovieRatingResponse(
            movie_id=None, 
            user_id=None,
            rating=None,
            success=False,
        )
    
    result = GetMovieRatingResponse(**result)
    return result


def get_user_info(req: UserInfoRequest) -> UserInfoResponse:

    get_rating_function_name = "get_user_info"
    result = get_user_rpc_client().send_task(get_rating_function_name, req)

    if not result:
        return UserInfoResponse(
            user_id=None, 
            username=None,
            email=None,
            role=None,
            registered_at=None,
            success=False,
        )
    
    result = UserInfoResponse(**result)
    return result

def get_recommendations_for_user(req: RecommendationRequest) -> RecommendationResponse:

    function_name = "get_recommendations"

    result = get_movie_rpc_client().send_task(function_name, req)

    if not result:
        return RecommendationResponse(
            movies=None, 
            success=False,
        )
    
    result = RecommendationResponse(**result)
    return result
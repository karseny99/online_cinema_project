import logging
import json

from rpc_client.rpc_client import get_user_rpc_client
from models.user_service_models import SetMovieRatingRequest, SetMovieRatingResponse, GetMovieRatingRequest, GetMovieRatingResponse, UserRoleRequest, UserRoleResponse

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


def get_role(req: UserRoleRequest) -> UserRoleResponse:

    get_rating_function_name = "get_user_role"
    result = get_user_rpc_client().send_task(get_rating_function_name, req)

    if not result:
        return UserRoleResponse(
            user_id=None, 
            role=None,
            success=False,
        )
    
    result = UserRoleResponse(**result)
    return result
import logging
import json

from rpc_client.rpc_client import get_user_rpc_client
from models.user_service_models import SetMovieRatingRequest, SetMovieRatingResponse

log = logging.getLogger(__name__)


def set_rating(req: SetMovieRatingRequest) -> SetMovieRatingResponse:
    set_rating_function_name = "set_movie_rating"
    rpc_client = get_user_rpc_client()

    result = str(rpc_client.send_task(set_rating_function_name, req))
    result = json.loads(result)
    result = SetMovieRatingResponse(**result)

    return result
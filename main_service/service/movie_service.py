from models.movie_service_models import ElasticRequest, ElasticResponse, MovieRequest, MovieInfoResponse
from rpc_client.rpc_client import get_movie_rpc_client

def get_movie_by_id(request: MovieRequest) -> MovieInfoResponse:
    '''
        Requests movie's info for given request
    '''

    search_function_name = "get_movie_info"
    print("sending request for movie")
    result = get_movie_rpc_client().send_task(search_function_name, request)

    result = MovieInfoResponse(**result)
    return result
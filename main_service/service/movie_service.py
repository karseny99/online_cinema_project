from models.movie_service_models import ElasticRequest, ElasticResponse, MovieItem
from rpc_client.rpc_client import get_movie_rpc_client

def search_movies(request: ElasticRequest) -> ElasticResponse:
    '''
        sends task to get movies by given requests
        Returns ElasticResponse-class 
        Returns None if timed out
    '''
    search_function_name = "search_movie"

    rpc_client = get_movie_rpc_client()
    
    result = rpc_client.send_task(search_function_name, request)
    result = ElasticResponse(**result)
    return result


def update_elastic_index() -> None:
    '''
        Sends task to update elastic-index, no waiting for result
    '''
    search_function_name = "update_index"
    rpc_client = get_movie_rpc_client()
    rpc_client.send_task_no_wait(search_function_name, None)

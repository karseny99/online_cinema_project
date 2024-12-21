from models.movie_service_models import ElasticRequest, ElasticResponse, MovieRequest, MovieInfoResponse
from rpc_client.rpc_client import get_elastic_rpc_client

def search_movies(request: ElasticRequest) -> ElasticResponse:
    '''
        sends task to get movies by given requests
        Returns ElasticResponse-class 
        Returns unsuccess ElasticResponse-class if timed out
    '''
    search_function_name = "search_movie"
    rpc_client = get_elastic_rpc_client()
    result = rpc_client.send_task(search_function_name, request)

    if not result:
        return ElasticResponse(movies=[], success=False)
    
    result = ElasticResponse(**result)
    return result


def update_elastic_index() -> None:
    '''
        Sends task to update elastic-index, no waiting for result
    '''
    function_name = "update_index"
    rpc_client = get_elastic_rpc_client()
    rpc_client.send_task_no_wait(function_name, None)


def get_movie_suggestions(request: ElasticRequest) -> ElasticResponse:
    '''
        Sends task to get elastic suggestions
    '''

    function_name = "get_suggestions"
    rpc_client = get_elastic_rpc_client()
    result = rpc_client.send_task(function_name, request)

    if not result:
        return ElasticResponse(movies=[], success=False)
    
    result = ElasticResponse(**result)
    return result

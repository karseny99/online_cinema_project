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

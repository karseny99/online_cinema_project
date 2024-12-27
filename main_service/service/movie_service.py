from models.movie_service_models import MovieRequest, MovieInfoResponse, GenresResponse
from rpc_client.rpc_client import get_movie_rpc_client

def get_movie_by_id(request: MovieRequest) -> MovieInfoResponse:
    '''
        Requests movie's info for given request
    '''

    search_function_name = "get_movie_info"
    result = get_movie_rpc_client().send_task(search_function_name, request)

    if not result:
        return MovieInfoResponse(movie=None, success=False)
    
    result = MovieInfoResponse(**result)
    return result

def get_distinct_genres() -> GenresResponse:
    '''
        Requests movie-genres in database
    '''

    search_function_name = "get_distinct_genres"
    result = get_movie_rpc_client().send_task(search_function_name)

    if not result:
        return GenresResponse(genres=None, success=False)
    
    result = GenresResponse(**result)
    return result

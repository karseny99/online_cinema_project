from app.services.elastic import ElasticSearch
from pydantic import ValidationError
from app.models.models import *

def elastic_search(query: ElasticRequest) -> ElasticResponse:
    ''' 
        Initializes index of elastic search
        Then searching for given query
        Returns list of movie items or None if not found

        See model file for movieItem
    '''
    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")
    # es_client.delete_index()
    es_client.load_to_index()
    # await es_client.check_index()

    try:
    # Выполнение поиска
        results = es_client.search(query.model_dump(exclude_none=True))
    except Exception as e:
        raise e
    finally:
        es_client.close()

    results = ElasticResponse(movies=[
        MovieItem(
            movie_id=movie.get('movie_id'),
            movie_title=movie.get('movie_title'),
            year=movie.get('year'),
            director=movie.get('director'),
            description=movie.get('description'),
            info_title=movie.get('info_title'),
            genres=movie.get('genres'),  # Проверка на список
            average_rating=movie.get('average_rating')
        ) for movie in results
        ],
        success=True
    )

    # Вывод результатов
    print("Found movie IDs:", results)
    
    return results

def elastic_update_index() -> ElasticResponse:
    ''' 
        Updates elastic index comparing num of movies in es-index and num of movies in database
    '''

    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")

    try:
        es_client.update_index_with_new_movies()
    except Exception as e:
        raise e
    finally:
        es_client.close()
        

def get_elastic_suggestions(query: ElasticRequest) -> ElasticResponse:
    '''
        Returns ElasticResponse of suggestions
        filled only movie_title  
    '''
    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")
    # es_client.delete_index()
    # es_client.load_to_index()
    # await es_client.check_index()

    try:
        results = es_client.get_suggestions(query.title)
    except Exception as e:
        raise e
    finally:
        es_client.close()

    results = ElasticResponse(movies=[
        MovieItem(
            movie_id=None,
            movie_title=title,
            year=None,
            description=None,
            info_title=None,
            genres=None,
            director=None,
            average_rating=None,
        ) for title in results
        ],
        success=True
    )
   
    return results

from app.service.elastic import ElasticSearch
from pydantic import ValidationError
from app.models.models import *

async def elastic_search(query: ElasticRequest) -> ElasticResponse:
    ''' 
        Initializes index of elastic search
        Then searching for given query
        Returns list of movie items or None if not found

        See model file for movieItem
    '''
    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")
    # es_client.delete_index()
    await es_client.load_to_index()
    # await es_client.check_index()

    try:
    # Выполнение поиска
        results = await es_client.search(query.model_dump(exclude_none=True))
    except Exception as e:
        raise e
    finally:
        await es_client.close()

    results = ElasticResponse(movies=[MovieItem(**movie) for movie in results])
    # Вывод результатов
    print("Found movie IDs:", results)
    
    return results

async def elastic_update_index() -> ElasticResponse:
    ''' 
        Updates elastic index comparing num of movies in es-index and num of movies in database
    '''

    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")

    try:
        es_client.update_index_with_new_movies()
    except Exception as e:
        raise e
    finally:
        await es_client.close()
        
# unused
# def parse_search_request(contract: BaseContractModel) -> ElasticRequest:
#     '''
#         Gets raw message and parse it into ElasticRequest class
#     '''
#     if contract.contract_type != "search_request":
#         raise ValueError("Invalid contract type")
    
#     try:
#         elastic_request = ElasticRequest(**contract.body)
#         return elastic_request
#     except ValidationError as e:
#         raise ValueError(f"Invalid body structure: {e}")
    
# def convert_to_base_contract(elastic_response: ElasticResponse) -> BaseContractModel:
#     '''
#         Internal class converts to base contract class
#     '''
#     return BaseContractModel(
#         contract_type="search_response",
#         body={"movies": elastic_response.movies},
#     )


# if __name__ == "__main__":
#     asyncio.run(elastic_search(search_query))
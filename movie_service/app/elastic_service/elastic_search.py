from app.elastic_service.elastic import ElasticSearch
from app.models.movie_item import MovieItem, SearchQueryElastic
from pydantic import ValidationError

async def elastic_search(query: SearchQueryElastic) -> list[MovieItem]:
    ''' 
        Initializes index of elastic search
        Then searching for given query
        Returns list of movie items or None if not found

        See model file for movieItem
    '''
    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")
    # es_client.delete_index()
    await es_client.load_to_index()
    await es_client.check_index()

    try:
    # Выполнение поиска
        results = await es_client.search(query.model_dump(exclude_none=True))
    except Exception as e:
        raise e
    finally:
        await es_client.close()

    results = [MovieItem(**movie) for movie in results]
    # Вывод результатов
    print("Found movie IDs:", results)
    
    return results


# if __name__ == "__main__":
#     asyncio.run(elastic_search(search_query))
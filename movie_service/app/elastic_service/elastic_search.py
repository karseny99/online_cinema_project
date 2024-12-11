from app.elastic_service.elastic import ElasticSearch
from app.models.movie_item import MovieItem

async def elastic_search(query: dict) -> list[str]:
    ''' 
        Initializes index of elastic search
        Then searching for given query
        Returns list of movie items or None if not found

        movie_item = {
            "movie_id": str,
            "title": str,
            "genres": list[str],

        }
    '''
    es_client = ElasticSearch(host="localhost", port=9200, index_name="movies")
    # es_client.delete_index()
    await es_client.load_to_index()
    await es_client.check_index()

    # Выполнение поиска
    results = await es_client.search(query)

    await es_client.close()

    results = [MovieItem(**movie) for movie in results]
    # Вывод результатов
    print("Found movie IDs:", results)
    
    return results


# if __name__ == "__main__":
#     asyncio.run(elastic_search(search_query))

from elasticsearch import ElasticsearchWarning, AsyncElasticsearch 
from app.repository.movie import get_movie_info
import warnings

class ElasticSearch:
    def __init__(self, host: str = "localhost", port: int = 9200, index_name: str = "movies"):
        warnings.filterwarnings("ignore", category=ElasticsearchWarning)
        self.es = AsyncElasticsearch(f"http://{host}:{port}")
        self.index_name = index_name

    async def close(self):
        await self.es.close()

    async def is_index_empty(self) -> bool:
        '''
            Return true if empty
            False otherwise
        '''    
        response = await self.es.count(index=self.index_name)
        return response['count'] == 0

    async def delete_index(self) -> None:
        '''
            Deletes the specified index along with all its documents
        '''
        if await self.es.indices.exists(index=self.index_name):
            await self.es.indices.delete(index=self.index_name)
            print(f"Index '{self.index_name}' has been deleted.")
        else:
            print(f"Index '{self.index_name}' does not exist.")


    async def create_index(self) -> None:
        '''
            Creates elastic index
        '''
        if not await self.es.indices.exists(index=self.index_name):
            mapping = {
                "mappings": {
                    "properties": {
                        "movie_id": {"type": "long"},
                        "movie_title": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "year": {"type": "integer"},
                        "director": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "description": {"type": "text"},
                        "info_title": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "genres": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "average_rating": {"type": "float"}
                    }
                }
            }
            await self.es.indices.create(index=self.index_name, body=mapping)
            

    async def load_to_index(self) -> None:
        '''
            Loading data from database to index
        '''
        await self.create_index()
        if not await self.is_index_empty():
            print("Index already exists!")
            return
        movies = await get_movie_info()
        print(f"Loading {len(movies)} movies to Elasticsearch...")
        for movie in movies:
            movie_dict = movie.__dict__
            movie_dict.pop('_sa_instance_state', None)
            await self.es.index(index=self.index_name, id=movie.movie_id, document=movie_dict)
        await self.es.indices.refresh(index=self.index_name)
        print(f"Index '{self.index_name}' has been refreshed.")


    async def create_if_empty(self) -> None:
        '''
            If index is empty then calling for creation
            Passing otherwise
        '''
        if await self.is_index_empty():
            await self.load_index()

    # Untested
    # async def update_index(self) -> None:
    #     '''
    #         Updates elastic index with new or modified movies
    #     '''
    #     movies = await get_movie_info()  
    #     actions = []
        
    #     for movie in movies:
    #         movie_dict = {
    #             "_op_type": "index", 
    #             "_index": self.index_name,
    #             "_id": movie.movie_id,
    #             "_source": {
    #                 "movie_id": movie.movie_id,
    #                 "movie_title": movie.movie_title,
    #                 "year": movie.year,
    #                 "director": movie.director,
    #                 "description": movie.description,
    #                 "info_title": movie.info_title,
    #                 "genres": movie.genres,
    #                 "average_rating": movie.average_rating
    #             }
    #         }
    #         actions.append(movie_dict)

    #     # Выполните пакетное обновление
    #     if actions:
    #         helpers.bulk(self.es, actions)

    #     # Обновите индекс, если это необходимо
    #     self.es.indices.refresh(index=self.index_name)


    async def search(self, query: dict) -> list:
        '''
            Searching for given request

            query = {
                "title": str,
                "year": int,      
                "genre": list of str,
                "director": str,

                "page": int,    
                "page_size": int,
            }

            Returns list of relevant movie items (check app.models.movie_item for pydantic model)
        '''
        
        es_query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": [],
                    "should": []  
                }
            }
        }

        if "title" in query:
            es_query["query"]["bool"]["should"].append({
                "match": {
                    "info_title": {
                        "query": query["title"],
                        "fuzziness": "AUTO"  # Автоматическая настройка нечеткости
                    }
                }
            })
            
            es_query["query"]["bool"]["should"].append({
                "prefix": {
                    "info_title": query["title"]  # Префиксный поиск
                }
        })


        # Adding filters
        if "year" in query:
            es_query["query"]["bool"]["filter"].append({
                "term": {
                    "year": query["year"]
                }
            })

        if "genre" in query:
            es_query["query"]["bool"]["filter"].append({
                "terms": {
                    "genres.keyword": query["genre"]
                }
            })

        if "director" in query:
            es_query["query"]["bool"]["filter"].append({
                "match": {
                    "director.keyword": query["director"]
                }
            })

        # Pagination
        page = query.get('page', 1)  # Устанавливаем значение по умолчанию
        page_size = query.get('page_size', 10)  # Устанавливаем значение по умолчанию
        from_ = (page - 1) * page_size
        size = page_size
        
        try:
            response = await self.es.search(index="movies", body=es_query, from_=from_, size=size)
        except Exception as e:
            print("Error during Elasticsearch search:", e)
            raise e
            
        return [hit["_source"] for hit in response["hits"]["hits"]]

    async def check_index(self):
        if await self.es.indices.exists(index=self.index_name):
            count = await self.es.count(index=self.index_name)
            print(f"Index '{self.index_name}' contains {count['count']} documents.")
        else:
            print(f"Index '{self.index_name}' does not exist.")

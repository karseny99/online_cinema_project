
from elasticsearch import Elasticsearch, NotFoundError
import repository.movies

class ElasticSearch:
    def __init__(self, host: str = "localhost", port: int = 9200, index_name: str = "movies"):
        self.es = Elasticsearch(f"http://{host}:{port}")
        self.index_name = index_name
        self.create_index()


    def is_index_empty(self) -> bool:
        '''
            Return true if empty
            False otherwise
        '''    
        response = self.es.count(index=self.index_name)
        return response['count'] == 0
    

    def create_index(self) -> None:
        '''
            Creates elastic index
        '''
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
        

    def load_to_index(self) -> None:
        '''
            Loading data from database to index
        '''
        movies = repository.movies.get_movies_full_info()
        for movie in movies:
            self.es.index(index="movies", id=movie["id"], document=movie)


    def create_if_empty(self) -> None:
        '''
            If index is empty then calling for creation
            Passing otherwise
        '''
        if self.is_index_empty():
            self.load_index()


    def search(self, query: dict) -> list:
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

            Returns list of relevant movie_ids
        '''
        
        es_query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            }
        }

        if "title" in query:
            es_query["query"]["bool"]["must"].append({
                "match": {
                    "title": query["title"]
                }
            })

        # Добавляем фильтры
        if "year" in query:
            es_query["query"]["bool"]["filter"].append({
                "term": {
                    "year": query["year"]
                }
            })

        if "genre" in query:
            es_query["query"]["bool"]["filter"].append({
                "terms": {
                    "genre": query["genre"]
                }
            })

        if "director" in query:
            es_query["query"]["bool"]["filter"].append({
                "match": {
                    "director": query["director"]
                }
            })

        # Pagination
        from_ = (query['page'] - 1) * query['page_size'] 
        size = query['page_size']

        response = self.es.search(index="movies", body=es_query, from_=from_, size=size)
        
        return [hit["_id"] for hit in response["hits"]["hits"]]


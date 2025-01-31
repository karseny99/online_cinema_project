from elasticsearch import ElasticsearchWarning, Elasticsearch 

from app.repository.movie import get_movies, get_movies_by_id_range
import warnings

class ElasticSearch:
    def __init__(self, host: str = "localhost", port: int = 9200, index_name: str = "movies"):
        warnings.filterwarnings("ignore", category=ElasticsearchWarning)
        self.es = Elasticsearch(f"http://{host}:{port}")
        self.index_name = index_name

    def close(self):
        self.es.close()

    def is_index_empty(self) -> bool:
        '''
            Return true if empty
            False otherwise
        '''    
        response = self.es.count(index=self.index_name)
        return response['count'] == 0

    def delete_index(self) -> None:
        '''
            Deletes the specified index along with all its documents
        '''
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
            print(f"Index '{self.index_name}' has been deleted.")
        else:
            print(f"Index '{self.index_name}' does not exist.")


    def create_index(self) -> None:
        '''
            Creates elastic index
        '''
        if not self.es.indices.exists(index=self.index_name):
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
                        "info_title_suggest": {
                            "type": "completion"
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
            self.es.indices.create(index=self.index_name, body=mapping)

            

    def load_to_index(self) -> None:
        '''
            Loading data from database to index
        '''
        self.create_index()
        if not self.is_index_empty():
            print("Index already exists!")
            return
        movies = get_movies()
        print(f"Loading {len(movies)} movies to Elasticsearch...")
        for movie in movies:
            movie_dict = movie.__dict__
            movie_dict.pop('_sa_instance_state', None)
            movie_dict['info_title_suggest'] = movie_dict['info_title']
            self.es.index(index=self.index_name, id=movie.movie_id, document=movie_dict)
        self.es.indices.refresh(index=self.index_name)
        print(f"Index '{self.index_name}' has been refreshed.")


    def create_if_empty(self) -> None:
        '''
            If index is empty then calling for creation
            Passing otherwise
        '''
        if self.is_index_empty():
            self.load_index()


    def get_movie_count(self) -> int:
        '''
            Returns num of items in elastic-index
        '''
        response = self.es.count(index=self.index_name)
        return response['count']



    def update_index_with_new_movies(self):
        # Получите количество фильмов в индексе
        current_count = self.get_movie_count()
        print(f"Текущее количество фильмов в индексе: {current_count}")

        # Получите новые фильмы из базы данных, начиная с movie_id = current_count + 1
        new_movies = get_movies_by_id_range(current_count + 1)

        if not new_movies:
            print("Нет новых фильмов для добавления в индекс.")
            return

        print(f"Добавление {len(new_movies)} новых фильмов в индекс...")

        for movie in new_movies:
            movie_dict = movie.__dict__
            movie_dict.pop('_sa_instance_state', None) 
            movie_dict['info_title_suggest'] = movie_dict['info_title']
            self.es.index(index=self.index_name, id=movie.movie_id, document=movie_dict)

        self.es.indices.refresh(index=self.index_name)  # Обновите индекс
        print(f"Индекс '{self.index_name}' обновлен с новыми фильмами.")


    def get_suggestions(self, title: str, limit: int = 10) -> list:
        '''
            Elastic's suggestions using Suggester.

            title: str - part of input
            limit: int - max count of suggestions

            Returns list of suggestions
        '''

        if not title:
            return []

        es_query = {
            "suggest": {
                "movie-suggest": {
                    "prefix": title,
                    "completion": {
                        "field": "info_title_suggest",
                        "fuzzy": {
                            "fuzziness": "AUTO"
                        },
                        "size": limit
                    }
                }
            }
        }

        try:
            response = self.es.search(index=self.index_name, body=es_query)
        except Exception as e:
            print("Error during Elasticsearch search for suggestions:", e)
            raise e

        suggestions = response.get("suggest", {}).get("movie-suggest", [])
        result = [option["text"] for suggestion in suggestions for option in suggestion["options"]]
        return result



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
            # Создаем фильтр для жанров
            genre_filter = {
                "bool": {
                    "must": [
                        {
                            "terms": {
                                "genres.keyword": query["genre"]
                            }
                        }
                    ],
                    "should": [
                        {
                            "terms": {
                                "genres.keyword": query["genre"]
                            }
                        }
                    ],
                    "minimum_should_match": 1  # хотя бы один жанр из запроса присутствует
                }
            }
            es_query["query"]["bool"]["filter"].append(genre_filter)


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
            response = self.es.search(index="movies", body=es_query, from_=from_, size=size)
        except Exception as e:
            print("Error during Elasticsearch search:", e)
            raise e
            
        return [hit["_source"] for hit in response["hits"]["hits"]]

    def check_index(self):
        if self.es.indices.exists(index=self.index_name):
            count = self.es.count(index=self.index_name)
            print(f"Index '{self.index_name}' contains {count['count']} documents.")
        else:
            print(f"Index '{self.index_name}' does not exist.")
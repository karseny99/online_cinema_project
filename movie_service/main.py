from app.elastic_service.elastic_search import elastic_search
import asyncio
from app.models.movie_item import SearchQueryElastic

example_query = SearchQueryElastic(
    title="Inception", 
    year=None, 
    genre=None, 
    director="Christopher Nolan",
    page=1,         
    page_size=10   
)

# search_query = {
#     "title": "Inception",
#     "year": 2010,
#     "genre": ["Sci-Fi"], # Also as select box   
#     "director": "Christopher Nolan", # Should be as selection in front
#     "page": 1,
#     "page_size": 10
# }



if __name__ == "__main__":
    asyncio.run(elastic_search(example_query))
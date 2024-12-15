from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from models.movie_service_models import ElasticRequest, BaseContractModel, ElasticResponse, MovieItem
from rpc_client.rpc_client import get_movie_rpc_client
from typing import List, Optional
import json 


router = APIRouter()

# @router.get("/movies/{movie_id}", response_class=HTMLResponse)
# async def get_movie_with_player(
#     movie_id: int,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     """
#     Эндпоинт для получения информации о фильме и плеера.
#     """
#     try:
#         movie_repo = MovieRepository(session)
#         movie_service = MovieService(movie_repo)
#
#         movie = await movie_service.get_movie_by_id(movie_id)
#         if not movie:
#             raise HTTPException(status_code=404, detail="Movie not found.")
#
#         movie_url = movie_service.fetch_movie_url(movie["title"])
#
#         return HTMLResponse(content=f"""
#         <html>
#             <body>
#                 <h1>{movie['title']}</h1>
#                 <p>Genres: {', '.join(movie['genres'])}</p>
#                 <video width="720" height="480" controls>
#                     <source src="{movie_url}" type="video/mp4">
#                     Your browser does not support the video tag.
#                 </video>
#             </body>
#         </html>
#         """, status_code=200)
#
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
#
#
@router.get("/movies", response_model=list[dict])
def get_all_movies(
        limit: int = 10,
        offset: int = 0,
):
    """
    Эндпоинт для получения списка всех фильмов с поддержкой пагинации.
    """
    try:

        movies = [
            {"id": 1,
             "title": "Star Wars. Episode 1",
             "genres": "Fantasy|Science fiction"
             },
            {"id": 2,
             "title": "Interstellar",
             "genres": "Fantasy"
             },
        ]
        return [
            {
                "id": movie["id"],
                "title": movie["title"],
                "genres": movie["genres"]
            }
            for movie in movies
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/search", response_model=ElasticResponse)
def search_movies(
    title: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[List[str]] = None,
    director: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    rpc_client = Depends(get_movie_rpc_client)
):
    """
        Эндпоинт для поиска фильмов с поддержкой пагинации.
    """
    try:
        request = ElasticRequest(
            title=title,
            year=year,
            genre=genre,
            director=director,
            page=page,
            page_size=page_size
        )

        # TODO: empty request validation
        contract_message = BaseContractModel(
            contract_type="search_request",  
            body=request  
        )
        contract_response: BaseContractModel = rpc_client.call(contract_message)
        if contract_response.contract_type == "search_response":
            movies_list = [MovieItem(**movie) for movie in contract_response.body['movies']]
            elastic_response = ElasticResponse(movies=movies_list)
            return elastic_response
        else:
            raise HTTPException(status_code=400, detail="Invalid contract type received.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

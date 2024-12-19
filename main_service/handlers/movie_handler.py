from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import List, Optional
import json 

from models.movie_service_models import ElasticRequest, ElasticResponse, MovieItem, MovieInfoResponse, MovieRequest
# from rpc_client.rpc_client import send_task
import service.movie_service
import service.elastic_service

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


# @router.get("/movies", response_model=list[dict])
# def get_all_movies(
#         limit: int = 10,
#         offset: int = 0,
# ):
#     """
#     Эндпоинт для получения списка всех фильмов с поддержкой пагинации.
#     """
#     try:

#         movies = [
#             {"id": 1,
#              "title": "Star Wars. Episode 1",
#              "genres": "Fantasy|Science fiction"
#              },
#             {"id": 2,
#              "title": "Interstellar",
#              "genres": "Fantasy"
#              },
#         ]
#         return [
#             {
#                 "id": movie["id"],
#                 "title": movie["title"],
#                 "genres": movie["genres"]
#             }
#             for movie in movies
#         ]

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/search", response_model=ElasticResponse)
def search_movies(
    title: Optional[str] = Query(None, min_length=1, description="Title of the movie"),
    year: Optional[int] = None,
    genre: Optional[List[str]] = None,
    director: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """
        Эндпоинт для поиска фильмов с поддержкой пагинации.
    """

    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    try:
        request = ElasticRequest(
            title=title,
            year=year,
            genre=genre,
            director=director,
            page=page,
            page_size=page_size
        )

        found_movies = service.elastic_service.search_movies(request) 
        if not found_movies.success:
            raise HTTPException(status_code=503, detail="Something went wrong. Please try again later.")
        return found_movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/movies/{movie_id}", response_model=MovieItem)
def get_movie_by_id(movie_id: int) -> MovieItem:
    '''
        Ручка для получения информации о фильме с данным movie_id
    '''

    try:
        request = MovieRequest(movie_id=movie_id)
        movie: MovieInfoResponse = service.movie_service.get_movie_by_id(request)
        if not movie.success:
            raise HTTPException(status_code=503, detail="Something went wrong. Please try again later.")
        
        # Movie not found
        if movie.movie is None:
            raise HTTPException(status_code=404, detail="Фильм не найден.")
        
        return movie.movie
    except ValueError as ve:
        # Пример обработки специфичной ошибки
        raise HTTPException(status_code=400, detail=f"Некорректный запрос: {str(ve)}")
    # except SomeSpecificException as se:
    #     # Обработка других специфичных исключений
    #     raise HTTPException(status_code=500, detail=f"Ошибка сервиса: {str(se)}")
    # except Exception as e:
    #     # Логирование и возврат 500 для всех остальных ошибок
    #     print(str(e))  # Здесь можно использовать логирование
    #     raise HTTPException(status_code=500, detail="Произошла ошибка на сервере.")

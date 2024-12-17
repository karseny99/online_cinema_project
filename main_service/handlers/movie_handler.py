from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import List, Optional
import json 

from models.movie_service_models import ElasticRequest, ElasticResponse, MovieItem
from models.models import BaseContractModel
# from rpc_client.rpc_client import send_task
import service.movie_service

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

        # found_movies = service.movie_service.find_movies(request) 
        found_movies = {'movies': [{'movie_id': 73447, 'movie_title': 'I Live My Life (1935)', 'year': 1935, 'director': 'W.S. Van Dyke', 'description': 'Kay, a bored society girl from New York, takes a trip to Greece, where she meets Terry, an archaeologist. She flirts with him and he falls for her. She heads back to New York and he follows...                See full summary\xa0»', 'info_title': 'I Live My Life', 'genres': ['Comedy', 'Romance'], 'average_rating': 2.5}, {'movie_id': 2587, 'movie_title': 'Life (1999)', 'year': 1999, 'director': 'Ted Demme', 'description': 'In 1932, two strangers are wrongfully convicted and develop a strong friendship in prison that lasts them through the 20th century.', 'info_title': 'Life', 'genres': ['Comedy', 'Crime', 'Drama'], 'average_rating': 2.925364758698092}, {'movie_id': 5324, 'movie_title': 'Life or Something Like It (2002)', 'year': 2002, 'director': 'Stephen Herek', 'description': "A reporter interviews a psychic, who tells her that she's going to die and her life is meaningless.", 'info_title': 'Life or Something Like It', 'genres': ['Comedy', 'Romance'], 'average_rating': 2.9371980676328504}, {'movie_id': 66240, 'movie_title': 'Dead Like Me: Life After Death (2009)', 'year': 2009, 'director': 'Stephen Herek', 'description': None, 'info_title': 'Dead Like Me: Life After Death', 'genres': ['Comedy', 'Fantasy'], 'average_rating': 2.98}, {'movie_id': 81107, 'movie_title': 'Wife! Be Like a Rose! (Tsuma yo bara no yo ni) (1935)', 'year': 1935, 'director': 'Mikio Naruse', 'description': None, 'info_title': 'Wife! Be Like a Rose!', 'genres': ['Drama'], 'average_rating': 3.375}, {'movie_id': 687, 'movie_title': 'Country Life (1994)', 'year': 1994, 'director': 'Michael Blakemore', 'description': 'Adaptation of Chekhov\'s "Uncle Vanya" set in rural Australia in the 1920\'s. Jack Dickens and his niece Sally run the family farm to support brother-in-law Alexander as a (supposedly ...                See full summary\xa0»', 'info_title': 'Country Life', 'genres': ['Drama', 'Romance'], 'average_rating': 2.995}, {'movie_id': 730, 'movie_title': 'Low Life (1994)', 'year': 1994, 'director': "John L'Ecuyer", 'description': None, 'info_title': 'Low Life', 'genres': ['Drama'], 'average_rating': 3.057142857142857}, {'movie_id': 1053, 'movie_title': 'Normal Life (1996)', 'year': 1996, 'director': 'John McNaughton', 'description': 'Chris is young idealistic cop who falls in love and gets married to Pam, a beautiful but emotionally unstable woman who suffers from alcoholism and drug addiction. While Chris is trying ...                See full summary\xa0»', 'info_title': 'Normal Life', 'genres': ['Crime', 'Drama', 'Romance'], 'average_rating': 3.035377358490566}, {'movie_id': 2624, 'movie_title': 'After Life (Wandafuru raifu) (1998)', 'year': 1998, 'director': 'Kore-eda Hirokazu', 'description': 'After death, people have a week to choose only one memory to keep for eternity.', 'info_title': 'After Life', 'genres': ['Drama', 'Fantasy'], 'average_rating': 3.9645669291338583}, {'movie_id': 3465, 'movie_title': "That's Life! (1986)", 'year': 1986, 'director': 'Blake Edwards', 'description': None, 'info_title': "That's Life!", 'genres': ['Drama'], 'average_rating': 2.73125}]}
        return found_movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

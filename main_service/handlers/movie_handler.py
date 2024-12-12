from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse

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

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional
import json 

from models.movie_service_models import ElasticRequest, ElasticResponse, MovieItem, MovieInfoResponse, MovieRequest, GenresResponse
# from rpc_client.rpc_client import send_task
import service.movie_service
import service.elastic_service

router = APIRouter()


@router.get("/search", response_model=ElasticResponse)
def search_movies(
    title: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    director: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """
        Эндпоинт для поиска фильмов с поддержкой пагинации.
    """
    print(f"Genre unsplit: {genre}")
    if genre:
        genre = genre.split(",")  # Разделяем строку на список

    print(f"Title: {title}, Year: {year}, Genre: {genre}, Director: {director}, Page: {page}, Page Size: {page_size}")
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


@router.get("/genres", response_model=GenresResponse)
def get_genres():
    '''
        Ручка для получения списка уникальных жанров, которые есть в бд
    '''
    genres = service.movie_service.get_distinct_genres()  # Вызов вашей функции для получения жанров
        
    if not genres.success:
        raise HTTPException(status_code=503, detail="Something went wrong. Please try again later.")
    return genres

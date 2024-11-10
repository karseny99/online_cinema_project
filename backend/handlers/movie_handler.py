from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.movie_service import MovieUseCase
from repositories.movie_repo import MovieRepository
from dto.movie_dto import MovieDTO
from typing import List

router = APIRouter()

# Функция для получения сессии базы данных
def get_db():
    from main import get_db
    return get_db()

@router.post("/movies/", response_model=MovieDTO)
def create_movie(title: str, genres: List[str], db: Session = Depends(get_db)):
    movie_use_case = MovieUseCase(MovieRepository(db))
    try:
        movie_use_case.create_movie(title, genres)
        return MovieDTO(id=1, title=title, genres=genres)  # Измените на реальный ид.
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/movies/{movie_id}", response_model=MovieDTO)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_use_case = MovieUseCase(MovieRepository(db))
    movie = movie_use_case.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieDTO(id=movie.id, title=movie.title, genres=movie.genres)

@router.get("/movies/", response_model=List[MovieDTO])
def list_movies(db: Session = Depends(get_db)):
    movie_use_case = MovieUseCase(MovieRepository(db))
    movies = movie_use_case.list_movies()
    return [MovieDTO(id=movie.id, title=movie.title, genres=movie.genres) for movie in movies]

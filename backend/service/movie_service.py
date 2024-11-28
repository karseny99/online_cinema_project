from typing import List, Optional
from repositories.movie_repo import MovieRepository

class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def fetch_movie_url(self, movie_title: str) -> str:
        """
        Генерация URL для воспроизведения фильма.
        """
        # Здесь можно использовать MinIO или другое хранилище
        # Предполагаем, что фильм хранится в бакете "moviess" с названием movie_title.mp4
        bucket_name = "moviess"
        file_name = f"{movie_title}.mp4"
        return f"http://localhost:9000/{bucket_name}/{file_name}"

    async def get_all_movies(self, limit: int = 10, offset: int = 0) -> List[dict]:
        """
        Получение списка всех фильмов с поддержкой пагинации.
        """
        return await self.movie_repository.get_all_movies(limit=limit, offset=offset)

    async def get_movie_by_id(self, movie_id: int) -> Optional[dict]:
        """
        Получение фильма по его ID.
        """
        movie = await self.movie_repository.get_movie_by_id(movie_id)
        if not movie:
            raise ValueError(f"Movie with ID {movie_id} not found.")
        return movie

    async def search_movies_by_title(self, title: str, limit: int = 10) -> List[dict]:
        """
        Поиск фильмов по названию.
        """
        return await self.movie_repository.search_movies_by_title(title, limit=limit)

    async def get_movies_by_genre(self, genre: str, limit: int = 10, offset: int = 0) -> List[dict]:
        """
        Получение фильмов по жанру с поддержкой пагинации.
        """
        return await self.movie_repository.get_movies_by_genre(genre, limit=limit, offset=offset)

    async def add_movie(self, title: str, genres: List[str]) -> int:
        """
        Добавление нового фильма.
        """
        if not title or not genres:
            raise ValueError("Title and genres must be provided.")
        return await self.movie_repository.add_movie(title=title, genres=genres)

    async def delete_movie(self, movie_id: int) -> bool:
        """
        Удаление фильма по ID.
        """
        success = await self.movie_repository.delete_movie(movie_id)
        if not success:
            raise ValueError(f"Movie with ID {movie_id} not found or could not be deleted.")
        return success

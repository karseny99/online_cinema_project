from sqlalchemy.sql import and_
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from core.minio_client import MinioClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import movies


class MovieRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.minio_client = MinioClient()

    def get_movie_url(self, movie_name: str) -> str:
        """Получить временную ссылку на фильм."""
        return self.minio_client.get_presigned_url(movie_name)

    async def get_all_movies(self, limit: int = 10, offset: int = 0) -> List[dict]:
        """
        Получение всех фильмов с поддержкой пагинации.
        """
        query = select(movies).limit(limit).offset(offset)
        result = await self.db.execute(query)
        rows = result.fetchall()  # Извлекаем строки результата
        return [
            {
                "id": row.id,
                "title": row.title,
                "genres": row.genres,
            }
            for row in rows
        ]

    async def get_movie_by_id(self, movie_id: int) -> Optional[dict]:
        """
        Получение фильма по ID.
        """
        stmt = select(movies).where(movies.c.id == movie_id)
        result = await self.db.execute(stmt)
        movie = result.fetchone()
        if movie:
            return {
                "id": movie.id,
                "title": movie.title,
                "genres": movie.genres,
            }
        return None

    async def search_movies_by_title(self, title: str, limit: int = 10) -> List[dict]:
        """
        Поиск фильмов по названию.
        """
        stmt = select(movies).where(movies.c.title.ilike(f"%{title}%")).limit(limit)
        result = await self.db.execute(stmt)
        rows = result.fetchall()
        return [
            {
                "id": row.id,
                "title": row.title,
                "genres": row.genres,
            }
            for row in rows
        ]

    async def get_movies_by_genre(self, genre: str, limit: int = 10, offset: int = 0) -> List[dict]:
        """
        Получение фильмов по жанру.
        """
        stmt = select(movies).where(movies.c.genres.any(genre)).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return [dict(row) for row in result.fetchall()]

    async def add_movie(self, title: str, genres: List[str]) -> int:
        """
        Добавление нового фильма.
        """
        stmt = movies.insert().values(title=title, genres=genres).returning(movies.c.id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def delete_movie(self, movie_id: int) -> bool:
        """
        Удаление фильма по ID.
        """
        stmt = movies.delete().where(movies.c.id == movie_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0



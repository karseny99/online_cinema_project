# app/repositories/movie_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import movies

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_movie(self, title: str, genres: list):
        stmt = movies.insert().values(title=title, genres=genres)
        self.db.execute(stmt)
        self.db.commit()
        return self.db.execute(select(movies).where(movies.c.title == title)).first()  # Возвращаем созданный объект

    def get_movie_by_id(self, movie_id: int):
        stmt = select(movies).where(movies.c.id == movie_id)
        return self.db.execute(stmt).first()

    def list_all_movies(self):
        stmt = select(movies)
        return self.db.execute(stmt).scalars().all()

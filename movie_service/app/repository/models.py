from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dataclasses import dataclass

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    
    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    imdb_id = Column(Integer, nullable=False)

    @classmethod 
    def from_orm(cls, movie_orm):
        return cls(
            movie_id = movie_orm.movie_id,
            title = movie_orm.title,
            imdb_id = movie_orm.imdb_id,
        )
    
class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    @classmethod 
    def from_orm(cls, genre_orm):
        return cls(
            genre_id = genre_orm.genre_id,
            name = genre_orm.name,
        )

class MoviesWithInfo(Base):
    __tablename__ = 'movies_with_info'

    movie_id = Column(Integer, primary_key=True)
    movie_title = Column(String, nullable=False)
    year = Column(Integer)
    director = Column(String(255))
    description = Column(Text)
    info_title = Column(String(255))
    genres = Column(ARRAY(String))  # Массив строк для жанров
    average_rating = Column(Float)   # Средний рейтинг
    
    @classmethod 
    def from_orm(cls, movie_orm):
        return cls(
            movie_id=movie_orm.movie_id,
            movie_title=movie_orm.movie_title,
            year=movie_orm.year,
            director=movie_orm.director,
            description=movie_orm.description,
            info_title=movie_orm.info_title,
            genres=movie_orm.genres,
            average_rating=movie_orm.average_rating,
        )

class Recommendation(Base):
    __tablename__ = 'recommendations'

    user_id = Column(Integer, primary_key=True) 
    movie_ids = Column(ARRAY(Integer)) 
    @classmethod 
    def from_orm(cls, recomend_orm):
        return cls(
            user_id=recomend_orm.user_id,
            movie_ids=recomend_orm.movie_ids,
        )
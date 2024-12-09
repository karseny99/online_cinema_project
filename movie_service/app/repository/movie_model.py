from sqlalchemy import Column, Integer, String, DateTime, Text
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
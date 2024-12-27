from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ARRAY, ForeignKey, TIMESTAMP
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
    

class Rating(Base):
    __tablename__ = 'ratings'
    
    rating_id = Column(Integer, primary_key=True)  
    user_id = Column(Integer)                       
    movie_id = Column(Integer)                      
    rating = Column(Float, nullable=False)          
    rated_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')  

   
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


class MovieGenre(Base):
    __tablename__ = 'movie_genre'
    
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)


class Recommendation(Base):
    __tablename__ = 'recommendations'

    user_id = Column(Integer, primary_key=True) 
    movie_ids = Column(ARRAY(Integer)) 

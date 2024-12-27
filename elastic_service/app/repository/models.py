from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MovieWithInfo(Base):
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

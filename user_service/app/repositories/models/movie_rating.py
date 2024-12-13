from sqlalchemy import Column, Integer, String, DateTime, MetaData, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MovieRating(Base):
    __tablename__ = 'ratings'

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    rated_at = Column(DateTime, default=datetime.now())

    @classmethod
    def from_orm(cls, movie_rating_orm):
        return cls(
            rating_id = movie_rating_orm.rating_id,
            user_id = movie_rating_orm.user_id,
            movie_id = movie_rating_orm.movie_id,
            rating = movie_rating_orm.rating,
            rated_ad = movie_rating_orm.rated_at
        )
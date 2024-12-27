import logging

from app.repositories.connector import *

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.models.movie_rating import MovieRating
from typing import List

class MovieRatingRepository:
    def __init__(self):
        pass

    def add_new_rating(self, movie_id: int, user_id: int, rating: float) -> int:
        '''
            Function adds new movie_rating to a database
            Returns a distinct rating_id
        '''
        with get_session() as session:

            existing_rating = session.query(MovieRating).filter_by(movie_id=movie_id, user_id=user_id).first()

            if existing_rating:
                # Если рейтинг существует, удаляем его
                session.delete(existing_rating)
                print(f"Existing rating with id {existing_rating.rating_id} has been deleted.")


            new_rating = MovieRating(
                movie_id=movie_id,
                user_id=user_id,
                rating=rating,
                rated_at=datetime.now()
            )

            session.add(new_rating)
            session.flush()  # Принудительно сохраняем объект, чтобы получить rating_id

            print(f"Rating with id {new_rating.rating_id} has been added to database")
            return new_rating.rating_id

    def get_rating_info(self, movie_id: int, user_id: int) -> MovieRating:
        '''
            Returns info about movie_rating with given movie_id, user_id
        '''
        with get_session() as session:
            rating = None
            try:
                rating = MovieRating.from_orm(session.query(MovieRating).filter(
                    MovieRating.movie_id == movie_id,
                    MovieRating.user_id == user_id
                ).one())
                rating = MovieRating.from_orm(rating)
            except NoResultFound:
                logging.info(f"Movie with movie_id {movie_id} not found in ratings")
            return rating

    def get_ratings_info(self, user_id: int) -> List[MovieRating]:
        '''
            Returns list of movies ratings for a given user_id
        '''
        with get_session() as session:
            ratings = []
            try:
                ratings_query = session.query(MovieRating).filter(
                    MovieRating.user_id == user_id
                ).all()

                ratings = [MovieRating.from_orm(rating) for rating in ratings_query]
            except NoResultFound:
                logging.info(f"No movie ratings found for user_id {user_id}")
            return ratings

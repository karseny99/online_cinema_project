from app.repositories.connector import *

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.models.movie_rating import MovieRating

class MovieRatingRepository:
    def __init__(self):
        pass

    def add_new_rating(self, movie_id: int, user_id: int, rating: float) -> int:
        '''
            Function adds new movie_rating to a database
            Returns a distinct rating_id
        '''

        new_rating = MovieRating(
            movie_id=movie_id,
            user_id=user_id,
            rating=rating,
            rated_at=datetime.now()
        )

        with get_session() as session:
            session.add(new_rating)
            session.flush()  # Принудительно сохраняем объект, чтобы получить rating_id

            print(f"Rating with id {new_rating.rating_id} has been added to database")
            return new_rating.rating_id

    def get_rating_info(self, movie_id: int, user_id: int) -> MovieRating:
        '''
            Returns info about movie_rating with given movie_id, user_id
        '''
        with get_session() as session:
            user = None
            try:
                user = MovieRating.from_orm(session.query(MovieRating).filter_by(movie_id == movie_id and user_id == user_id).one())
                return user
            except NoResultFound:
                print(f"Movie with movie_id {movie_id} not found in ratings")

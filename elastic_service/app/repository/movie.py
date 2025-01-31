
from sqlalchemy.future import select

from app.repository.database import *
from app.repository.models import MovieWithInfo


@connection
def get_movies(session) -> list:
    '''
        Returns all films from database
    '''
    result = session.execute(select(MovieWithInfo))
    movies = result.scalars().all()
    return movies


@connection
def get_movies_by_id_range(session, start_id: int) -> list:
    '''
        Returns list of movies from range: start_id + 1 till the end
    '''
    result = session.execute(select(MovieWithInfo).where(MovieWithInfo.movie_id > start_id))
    return result.scalars().all()


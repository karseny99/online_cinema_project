from sqlalchemy.future import select
from sqlalchemy import distinct
from app.repository.database import *
from app.repository.models import MoviesWithInfo, Genre


@connection
def get_movie_by_id(session, movie_id: int) -> MoviesWithInfo:
    '''
        Returns MovieWithInfo by movie_id
    '''
    result = session.execute(select(MoviesWithInfo).where(MoviesWithInfo.movie_id==movie_id))
    movies = result.one_or_none()

    if movies:
        movies = MoviesWithInfo.from_orm(movies[0])
    return movies


@connection
def get_distinct_genres(session) -> list[str]:
    '''
        Returns distinct genre's names
    '''
    genres = session.execute(select(distinct(Genre.name)))
    return [row[0] for row in genres]

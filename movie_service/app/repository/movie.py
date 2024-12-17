from sqlalchemy.future import select

from app.repository.database import *
from app.repository.models import MoviesWithInfo
import asyncio


@connection
async def get_movie_by_id(session, movie_id: int) -> MoviesWithInfo:
    '''
        Returns MovieWithInfo by movie_id
    '''
    result = await session.execute(select(MoviesWithInfo).where(MoviesWithInfo.movie_id==movie_id))
    movies = result.one_or_none()

    if movies:
        movies = MoviesWithInfo.from_orm(movies[0])
    return movies


# @connection
# async def get_movies_by_id_range(session, start_id: int):
#     '''
#         Returns list of movies from range: start_id + 1 till the end
#     '''
#     result = await session.execute(select(MovieWithInfo).where(MovieWithInfo.movie_id > start_id))
#     return result.scalars().all()

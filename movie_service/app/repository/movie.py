from app.repository.connector import *
from app.repository.movie_model import *

from sqlalchemy.future import select

async def get_movie_info() -> list:
    '''
        returns info about all movies from view movie_with_info
    ''' 

    async with get_session() as session:
        result = await session.execute(select(MoviesWithInfo))
        movies = result.scalars().all()
        return [MoviesWithInfo.from_orm(movie) for movie in movies]




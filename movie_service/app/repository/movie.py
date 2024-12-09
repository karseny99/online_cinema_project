from app.repository.connector import *
from app.repository.movie_model import Movie

from sqlalchemy.future import select

async def get_movie_info() -> list:
    '''
        returns info about all movies in database
    ''' 

    async with get_session() as session:
        select_stmt = select(Movie)
        result = await session.execute(select_stmt)
        
        movies = [Movie.from_orm(movie) for movie in result.scalars().all()]
        for movie in movies[:10]:
            print(movie.__dict__)



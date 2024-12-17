
from sqlalchemy.future import select

from app.repository.database import *
from app.repository.models import MovieWithInfo


@connection
async def get_movies(session):
    '''
        Returns all films from database
    '''
    return await session.execute(select(MovieWithInfo))

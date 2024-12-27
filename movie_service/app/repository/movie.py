from sqlalchemy.future import select
from sqlalchemy import distinct, desc
from app.repository.database import *
from app.repository.models import MoviesWithInfo, Genre, Recommendation


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


@connection
def get_recommendations(session, user_id: int) -> list[MoviesWithInfo]:
    '''
        
    '''

    query = select(Recommendation).where(Recommendation.user_id == user_id)
    result = session.execute(query)

    recommendation = result.one_or_none()

    if not recommendation:
        print(f"{user_id} wasn't found")
        return None 
    
    recommendation_data = recommendation[0]
    movie_ids = recommendation_data.movie_ids

    # Получаем информацию о фильмах по массиву movie_ids
    if movie_ids:
        movies_query = select(MoviesWithInfo).where(MoviesWithInfo.movie_id.in_(movie_ids))
        movies_result = session.execute(movies_query)
        
        movies = [MoviesWithInfo.from_orm(movie) for movie in movies_result.scalars().all()]
        return movies

    return None



@connection
def get_top_movies(session, limit: int = 100) -> list[MoviesWithInfo]:
    '''
        
    '''
    result = session.execute(
        select(MoviesWithInfo)
        .where(MoviesWithInfo.year >= 1980)
        .where(MoviesWithInfo.average_rating.isnot(None))  # Исключаем фильмы с NULL рейтингом
        .where(MoviesWithInfo.average_rating <= 5)
        .order_by(desc(MoviesWithInfo.average_rating))
        .limit(limit)
    )
    
    movies = result.scalars().all()

    return [MoviesWithInfo.from_orm(movie) for movie in movies]

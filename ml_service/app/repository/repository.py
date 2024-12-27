from sqlalchemy.future import select
from sqlalchemy import distinct
from app.repository.database import *
from app.repository.models import Rating, Genre, Movie, MovieGenre, Recommendation
import pandas as pd


@connection
def get_ratings_in_batches(session, batch_size: int, save_path: str) -> None:
    offset = 0
    while True:
        print(f"current: {offset}")
        query = select(Rating).limit(batch_size).offset(offset)
        result = session.execute(query)
        
        ratings_list = result.scalars().all() 
        
        if not ratings_list:
            break
        
        df = pd.DataFrame([{
            'rating_id': rating.rating_id,
            'user_id': rating.user_id,
            'movie_id': rating.movie_id,
            'rating': rating.rating,
            'rated_at': rating.rated_at
        } for rating in ratings_list])
        
        df.to_csv(save_path, mode='a', header=not bool(offset), index=False)
        offset += batch_size


@connection
def export_movies_to_csv(session, batch_size: int) -> None:
    offset = 0
    while True:
        print(f"Exporting movies, current offset: {offset}")
        query = select(Movie).limit(batch_size).offset(offset)
        result = session.execute(query)
        
        movies_list = result.scalars().all()
        
        if not movies_list:
            break
        
        df = pd.DataFrame([{
            'movie_id': movie.movie_id,
            'title': movie.title,
            'imdb_id': movie.imdb_id
        } for movie in movies_list])
        
        df.to_csv("movies.csv", mode='a', header=not bool(offset), index=False)
        offset += batch_size


@connection
def export_genres_to_csv(session, batch_size: int) -> None:
    offset = 0
    while True:
        print(f"Exporting genres, current offset: {offset}")
        query = select(Genre).limit(batch_size).offset(offset)
        result = session.execute(query)
        
        genres_list = result.scalars().all()
        
        if not genres_list:
            break
        
        df = pd.DataFrame([{
            'genre_id': genre.genre_id,
            'name': genre.name
        } for genre in genres_list])
        
        df.to_csv("genres.csv", mode='a', header=not bool(offset), index=False)
        offset += batch_size


@connection
def export_movie_genres_to_csv(session, batch_size: int) -> None:
    offset = 0
    while True:
        print(f"Exporting movie_genres, current offset: {offset}")
        query = select(MovieGenre).limit(batch_size).offset(offset)
        result = session.execute(query)
        
        movie_genres_list = result.scalars().all()
        
        if not movie_genres_list:
            break
        
        df = pd.DataFrame([{
            'movie_id': movie_genre.movie_id,
            'genre_id': movie_genre.genre_id
        } for movie_genre in movie_genres_list])
        
        df.to_csv("movie_genres.csv", mode='a', header=not bool(offset), index=False)
        offset += batch_size


@connection
def get_unique_movies(session) -> list[int]:
    '''
        Returns list of distinct movie_ids
    '''

    query = select(distinct(Movie.movie_id))
    result = session.execute(query)

    movie_ids = result.scalars().all()
    return movie_ids


@connection
def update_database_recommendations(session, new_data):
    '''
        Updates for pool of given users their movie_recommendations
    '''
    print("Updating database")
    new_data = [Recommendation(user_id=item[0], movie_ids=item[1]) for item in new_data]
    session.bulk_save_objects(new_data)
    session.commit()


@connection
def get_rated_movies(session, user_list) -> dict:
    '''
        Gets for all users in user_list their rated lists
    '''

    rated_movies = {}

    results = session.query(Rating).filter(Rating.user_id.in_(user_list)).all()

    # Обрабатываем результаты
    for rating in results:
        user_id = rating.user_id
        movie_id = rating.movie_id
        
        if user_id not in rated_movies:
            rated_movies[user_id] = []
        
        rated_movies[user_id].append(movie_id)

    return rated_movies

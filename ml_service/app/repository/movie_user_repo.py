import pandas as pd
import numpy as np

def get_ratings(ratings_path: str, max_rows: int = 1000000) -> pd.DataFrame:
    """
    Загружает и подготавливает таблицу рейтингов.
    """
    df = pd.read_csv(ratings_path, nrows=max_rows)
    df.rename(columns={'userId': 'user_id', 'movieId': 'movie_id'}, inplace=True)
    df.drop(['timestamp'], axis=1, inplace=True)
    return df

def get_movies(movies_path: str) -> pd.DataFrame:
    """
    Загружает и подготавливает таблицу фильмов.
    """
    df = pd.read_csv(movies_path)
    df.rename(columns={'movieId': 'movie_id', 'title': 'title'}, inplace=True)
    df.drop(['genres'], axis=1, inplace=True)
    return df

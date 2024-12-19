import pandas as pd
import numpy as np

def get_relevance_matrix_path() -> str:
    """
    Возвращает путь к файлу для сохранения матрицы.
    """
    return "relevance_matrix.csv"

def save_relevance_matrix(relevance_matrix: pd.DataFrame, file_path: str) -> None:
    """
    Сохраняет матрицу релевантности в CSV.
    """
    relevance_matrix.to_csv(file_path, index=True)

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

def run_pipeline(recommendation_system):
    """
    Запускает процесс рекомендаций.
    """
    relevance_matrix = recommendation_system.run_recommendation_pipeline()

    file_path = get_relevance_matrix_path()

    save_relevance_matrix(relevance_matrix, file_path)

    # print(relevance_matrix.head())
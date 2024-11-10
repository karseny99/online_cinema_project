
from repositories.movie_repo import MovieRepository

class MovieUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def create_movie(self, title: str, genres: list):
        return self.movie_repository.create_movie(title, genres)

    def get_movie(self, movie_id: int):
        return self.movie_repository.get_movie_by_id(movie_id)

    def list_movies(self):
        return self.movie_repository.list_all_movies()


import logging

import logging

import app.repository.movie
from app.models.models import MovieItem, MovieInfoResponse, GenresResponse
from s3.movie import S3Repository

s3_url = "localhost:9000"
movie_posters_s3_bucket = "posters"
movies_s3_bucket = "movies"

log = logging.getLogger(__name__)

class MovieService:

    def get_movie_by_id(movie_id: int) -> MovieInfoResponse:
        '''
            Returns MovieItem for given movie_id
            None-response if unexisted movie_id was received
        '''

        movie = app.repository.movie.get_movie_by_id(movie_id=movie_id)
        if not movie:
            return MovieInfoResponse(movie=None, success=True)
        log.info(movie)
        movie = MovieItem.from_orm(movie)
        movie = MovieInfoResponse(movie=movie, success=True)

        try:
            movie_s3 = S3Repository()
            movie_urls_dict = movie_s3.get_url(movie.movie.movie_title)
            movie.movie.movie_url = movie_urls_dict["movie_url"]
            movie.movie.movie_poster_url = movie_urls_dict["movie_poster_url"]
        except Exception as e:
            log.info(f"connection to s3 error: {e}")

        log.info(f"movie_url: {movie.movie.movie_url}\nmovie_poster_url:{movie.movie.movie_poster_url}")
        return movie

    def get_distinct_genres() -> GenresResponse:
        '''
            Returns distinct list of genres from database in GenresResponse type
        '''

        genres = app.repository.movie.get_distinct_genres()

        if not genres:
            return GenresResponse(genres=None, success=True)

        genres = GenresResponse(genres=genres, success=True)
        return genres

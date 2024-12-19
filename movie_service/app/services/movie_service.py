
import app.repository.movie
from app.models.models import MovieItem, MovieInfoResponse, GenresResponse
class MovieService:

    def get_movie_by_id(movie_id: int) -> MovieInfoResponse:
        '''
            Returns MovieItem for given movie_id
            None-response if unexisted movie_id was received
        '''

        movie = app.repository.movie.get_movie_by_id(movie_id=movie_id)
        if not movie:
            return MovieInfoResponse(movie=None, success=True)

        movie = MovieItem.from_orm(movie)
        movie = MovieInfoResponse(movie=movie, success=True)
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
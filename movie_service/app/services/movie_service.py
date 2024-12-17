
import app.repository.movie
from app.models.models import MovieItem, MovieInfoResponse
class MovieService:

    def get_movie_by_id(movie_id: int) -> MovieInfoResponse:
        '''
            Returns MovieItem for given movie_id
            None if unexisted movie_id was received
        '''

        movie = app.repository.movie.get_movie_by_id(movie_id=movie_id)
        movie = MovieItem.from_orm(movie)
        movie = MovieInfoResponse(movie=movie)
        return movie

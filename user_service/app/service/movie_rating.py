from pyexpat.errors import messages

from app.repositories.movie_rating import MovieRatingRepository
from app.models.models import SetMovieRatingRequest, SetMovieRatingResponse, GetMovieRatingRequest, GetMovieRatingResponse
import logging

log = logging.getLogger(__name__)

class MovieRatingService:
    def __init__(self):
        self.movie_rating_repository = MovieRatingRepository()

    def new_rating(self, req: SetMovieRatingRequest) -> SetMovieRatingResponse:
        try:
            rating_id = self.movie_rating_repository.add_new_rating(
                movie_id=req.movie_id,
                user_id=req.user_id,
                rating=req.rating,
            )
            if rating_id:
                log.info(f"New rating: {req.rating} by user: {req.user_id} to movie: {req.movie_id}")
                return SetMovieRatingResponse(
                    user_id=req.user_id,
                    movie_id=req.movie_id,
                    success=True,
                    message='ok'
                )
            else:
                log.error(f"Error: rating id is invalid: {rating_id}")
                return SetMovieRatingResponse(
                    user_id=req.user_id,
                    movie_id=req.movie_id,
                    success=False,
                    message=f"Error: rating id is invalid: {rating_id}"
                )
        except Exception as e:
            return SetMovieRatingResponse(
                user_id=req.user_id,
                movie_id=req.movie_id,
                success=False,
                message=e
            )
        
    def get_rating(self, req: GetMovieRatingRequest) -> GetMovieRatingResponse:

            '''
                Returns for given movie_id and user_id rating
            '''

            result = self.movie_rating_repository.get_rating_info(movie_id=req.movie_id, user_id=req.user_id)
            if not result:
                return GetMovieRatingResponse(
                    movie_id=req.movie_id, 
                    user_id=req.user_id, 
                    rating=None, 
                    success=True,
                )
            return GetMovieRatingResponse(
                movie_id=result.movie_id, 
                user_id=result.user_id, 
                rating=result.rating, 
                success=True,
            )

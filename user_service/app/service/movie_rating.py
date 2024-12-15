from app.repositories.movie_rating import MovieRatingRepository
from app.models.models import SetMovieRatingRequest, SetMovieRatingResponse
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
                return SetMovieRatingResponse(user_id=req.user_id, movie_id=req.movie_id, success=True)
            else:
                log.error(f"Error: rating id is invalid: {rating_id}")
                return SetMovieRatingResponse()
        except Exception as e:
            print(f"Exception: {e}")
            return SetMovieRatingResponse()
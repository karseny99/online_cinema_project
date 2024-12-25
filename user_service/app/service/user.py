from passlib.context import CryptContext
from jose import JWTError, jwt
import app.repositories.user, app.repositories.movie_rating
from datetime import datetime, timedelta
from app.models.models import UserInfoResponse, UserInfoRequest, Movie


class UserService:
    def __init__(self):
        self.movie_rating_repository = app.repositories.movie_rating.MovieRatingRepository()

    def get_user_info(self, request: UserInfoRequest) -> UserInfoResponse:
        '''
            Calls db function for user's info
        '''
        user_info = app.repositories.user.get_user_info(request.user_id)
        ratings_info = self.movie_rating_repository.get_ratings_info(request.user_id)
        ratings_info = [Movie(
            movie_id=movie.movie_id,
            movie_title="",
            rating=movie.rating_id,
        ) for movie in ratings_info]

        if not user_info:
            return UserInfoResponse(
                user_id=None,
                username=None,
                email=None,
                role=None,
                registered_at=None,
                ratings=None,
                success=False,
            )

        return UserInfoResponse(
            user_id=user_info.user_id,
            username=user_info.username,
            email=user_info.email,
            role=user_info.role,
            registered_at=user_info.registered_at,
            ratings=ratings_info,
            success=True,
        )

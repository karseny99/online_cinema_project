from passlib.context import CryptContext
from jose import JWTError, jwt
import app.repositories.user 
from datetime import datetime, timedelta
from app.models.models import UserInfoResponse, UserInfoRequest


def get_user_info(request: UserInfoRequest) -> UserInfoResponse:
    '''
        Calls db function for user's info
    '''
    result = app.repositories.user.get_user_info(request.user_id)

    if not result:
        return UserInfoResponse(
            user_id=None, 
            username=None,
            email=None,
            role=None,
            registered_at=None,
            success=False,
        )
    
    return UserInfoResponse(
            user_id=result.user_id, 
            username=result.username,
            email=result.email,
            role=result.role,
            registered_at=result.registered_at,
            success=True,
        )

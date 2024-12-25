from passlib.context import CryptContext
from jose import JWTError, jwt
import app.repositories.user 
from datetime import datetime, timedelta
from app.models.models import UserRoleRequest, UserRoleResponse


def get_user_role(request: UserRoleRequest) -> UserRoleResponse:
    '''
        Calls db function for user's role
    '''
    print(f"given request: {request}")
    result = app.repositories.user.get_user_role(request.user_id)

    if not result:
        return UserRoleResponse(
            user_id=request.user_id,
            role=None, 
            success=False,
        )
    
    return UserRoleResponse(user_id=request.user_id, role=result, success=True)
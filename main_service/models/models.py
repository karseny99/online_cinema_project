from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class BaseRequest(BaseModel):
    request_id: str
    source: str

class BaseResponse(BaseModel):
    request_id: str
    status: str
    message: Optional[str]

class RegisterRequest(BaseRequest):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)
    email: EmailStr
    full_name: Optional[str]

class RegisterResponse(BaseResponse):
    user_id: Optional[str]

class LoginRequest(BaseRequest):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)

class LoginResponse(BaseResponse):
    access_token: str   # JWT
    token_type: str     # bearer

class GetMoviesRequest(BaseRequest):
    filters: Optional[List]

class GetMoviesResponse(BaseResponse):
    movies: List


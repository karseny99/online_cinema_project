from pydantic import BaseModel, constr, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)
    email: EmailStr
    full_name: Optional[str]


class RegisterResponse(BaseModel):
    user_id: int
    message: str


class LoginRequest(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)


class LoginResponse(BaseModel):
    access_token: str  # JWT
    token_type: str  # bearer
    message: str

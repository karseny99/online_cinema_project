import http
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response
from models.models import *
from service.auth_service import *

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, response: Response):
    try:
        auth_service = AuthService()
        user_id = auth_service.register_user(
            email=request.email,
            username=request.username,
            password=request.password,
            role="reader"
        )

        resp = RegisterResponse(
            request_id=request.request_id,
            status=http.HTTPStatus.OK,
            message="User registered successfully!",
            user_id=str(user_id),
        )
        response.status_code = http.HTTPStatus.OK
        return resp
    except (UsernameExistsException, EmailExistsException) as e:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        return RegisterResponse(
            request_id=request.request_id,
            status=http.HTTPStatus.BAD_REQUEST,
            message=str(e),
            user_id=None
        )
    except Exception as e:
        response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        return RegisterResponse(
            request_id=request.request_id,
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            message=f"Internal server error: {str(e)}",
            user_id=None
        )


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response):
    auth_service = AuthService()

    try:
        user = auth_service.authenticate_user(username=request.username, password=request.password)
        if not user:
            response.status_code = http.HTTPStatus.BAD_REQUEST
            return LoginResponse(
                request_id=request.request_id,
                status=http.HTTPStatus.BAD_REQUEST,
                message="Incorrect username or password!",
                access_token="",
                token_type=""
            )

        access_token = auth_service.create_access_token(data={"sub": user.username})
        response.status_code = http.HTTPStatus.OK
        return LoginResponse(
            request_id=request.request_id,
            status=http.HTTPStatus.OK,
            message="Login successful!",
            access_token=access_token,
            token_type="bearer"
        )
    except Exception as e:
        response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        return LoginResponse(
            request_id=request.request_id,
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            message=f"An error occurred: {str(e)}",
            access_token="",
            token_type=""
        )
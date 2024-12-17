import http
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response

import service.auth_service
from models.models import *
from service.auth_service import *

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, response: Response):
    resp = service.auth_service.register_user(req=request)

    if resp.message == "registered successfully!":
        response.status_code = http.HTTPStatus.OK
    elif resp.message == "username already exists" or resp.message == "email already exists":
        response.status_code = http.HTTPStatus.BAD_REQUEST
    else:
        response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR

    response.body = resp
    return resp


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response):
    resp = service.auth_service.login_user(req=request)

    response.body = resp
    if resp.message == "user does not exist":
        response.status_code = http.HTTPStatus.BAD_REQUEST
    elif resp.message == "token created successfully!":
        response.status_code = http.HTTPStatus.OK
    else:
        response.status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR

    return resp

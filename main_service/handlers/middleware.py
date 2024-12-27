import logging

from fastapi import FastAPI, Request, HTTPException, Depends
from jose import jwt, JWTError
from core.config import settings
from starlette.responses import JSONResponse
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse

log = logging.getLogger(__name__)


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        log.info(f"Request URL: {request.url}")
        log.info(f"Cookies in request: {request.cookies}")
        if request.url.path in [
            "/auth/login",
            "/auth/register",
            "/static/styles.css",
            "/favicon.ico",
        ]:
            return await call_next(request)

        token = request.cookies.get("jwt_token")
        log.info(f"middleware: token got: {request.cookies.get('jwt_token')}")
        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization token missing"}
            )

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
            request.state.user = payload  # Сохраняем данные пользователя в запросе
        except JWTError as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Invalid or expired token: {e}"}
            )

        return await call_next(request)


def get_current_user(request: Request):
    if not hasattr(request.state, "user") or request.state.user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request.state.user


class RedirectOnExpiredTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.status_code == 401 and response.headers.get("content-type") == "application/json":
            return RedirectResponse(url="/auth/login")

        return response

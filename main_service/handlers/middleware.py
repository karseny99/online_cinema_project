from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from core.config import settings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/auth/login", "/auth/register"]:  # Список эндпоинтов, которые не требуют проверки
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing or invalid"}
            )

        token = auth_header.split(" ")[1]

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
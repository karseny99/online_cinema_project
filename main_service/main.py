from wsgiref.util import request_uri

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from handlers.middleware import JWTMiddleware, RedirectOnExpiredTokenMiddleware, get_current_user
from handlers.movie_handler import router as movie_router
from handlers.auth import router as auth_router
from handlers.user_handler import router as user_router
from handlers.ping import router as ping_router
from handlers.user_handler import get_user_info
from handlers.movie_upload import router as movie_upload_router
import uvicorn

app = FastAPI()
app.add_middleware(JWTMiddleware)
app.add_middleware(RedirectOnExpiredTokenMiddleware)

templates = Jinja2Templates(directory="../frontend/templates")
# app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.mount("/static", StaticFiles(directory="../frontend/templates/static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(movie_router, prefix="/api", tags=["movies catalog"])
app.include_router(user_router, prefix="/api", tags=["set movie rating"])
app.include_router(ping_router, prefix="/api", tags=["ping"])
app.include_router(movie_upload_router, prefix="/api", tags=["movies upload"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse("page_not_found.html", {"request": request, "message": "Некорректный запрос. Пожалуйста, проверьте введенные данные."}, status_code=422)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def read_search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/movies/{movie_id}", response_class=HTMLResponse)
async def movie_detail_page(movie_id: int, request: Request):
    return templates.TemplateResponse("movie_detail.html", {"request": request, "movie_id": movie_id})

@app.get("/auth/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request":  request})

@app.get("/auth/login", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("login.html", {"request":  request})

@app.get("/profile", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("user_profile.html", {"request":  request})

@app.get("/feed", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("feed.html", {"request":  request})


def is_admin(current_user: dict = Depends(get_current_user)):
    user_role_response = get_user_info(current_user)
    print(user_role_response.role)
    if user_role_response.role != "admin":
        raise HTTPException(status_code=403, detail="Access Denied")

@app.get("/admin_panel", response_class=HTMLResponse)
async def monitoring(request: Request, user: dict = Depends(is_admin)):
    return templates.TemplateResponse("admin_panel.html", {"request": request})


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    return templates.TemplateResponse("page_not_found.html", {"request": request, "message": "Страница не найдена."})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
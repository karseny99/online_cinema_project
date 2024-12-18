from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from handlers.middleware import JWTMiddleware
from handlers.movie_handler import router as movie_router
from handlers.auth import router as auth_router
from handlers.user_handler import router as user_router
import uvicorn

app = FastAPI()
app.add_middleware(JWTMiddleware)

templates = Jinja2Templates(directory="../frontend/templates")
# app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(movie_router, prefix="/api", tags=["movies catalog"])
app.include_router(user_router, prefix="/api", tags=["set movie rating"])
# TODO: other routes

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
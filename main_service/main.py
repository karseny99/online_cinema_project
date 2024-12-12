from fastapi import FastAPI
from handlers.movie_handler import router as movie_router
from handlers.auth import router as auth_router
import uvicorn

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(movie_router, prefix="/api", tags=["movies catalog"])
# TODO: other routes

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
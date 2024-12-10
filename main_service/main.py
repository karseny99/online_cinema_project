from fastapi import FastAPI
# from handlers.movie_handler import router as movie_router
from handlers.auth import router as auth_router
import uvicorn

app = FastAPI()

# app.include_router(movie_router, prefix="/api")
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# TODO: other routes

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from fastapi.middleware.cors import CORSMiddleware
import vlc
import os
import threading
import uvicorn

# from handlers.user_handler import router as user_router
from handlers.movie_handler import router as movie_router
from handlers.auth import router as auth_router

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Укажите, какие источники разрешены
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(user_router, prefix="/api")
app.include_router(movie_router, prefix="/api")
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# TODO: other routes
# app.include_router(tag_router, prefix="/api")
# app.include_router(rating_router, prefix="/api")

# @app.get("/")
# async def root():
#     return {"message": "Welcome to our online cinema!"}
#

# app.include_router(movie_routes.router, prefix="/movies", tags=["Movies"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
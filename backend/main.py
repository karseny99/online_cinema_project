from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from fastapi.middleware.cors import CORSMiddleware
import vlc
import os
import threading
import uvicorn

from handlers.user_handler import router as user_router
from handlers.movie_handler import router as movie_router


# from app.controllers.tag_controller import router as tag_router
# from app.controllers.rating_controller import router as rating_router

DATABASE_URL = "postgresql+asyncpg://pg-user:pg-password@localhost:5432/cinema-db?sslmode=false"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Укажите, какие источники разрешены
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(user_router, prefix="/api")
app.include_router(movie_router, prefix="/api")

# TODO: other routes
# app.include_router(tag_router, prefix="/api")
# app.include_router(rating_router, prefix="/api")

# @app.get("/")
# async def root():
#     return {"message": "Welcome to our online cinema!"}
#

video_player = None

def play_video(video_path):
    global video_player
    if video_player is None:
        video_player = vlc.MediaPlayer(video_path)
        video_player.play()
VIDEO_PATH = 'movies_storage/Dire Straits - Sultans Of Swing (SHRED VERSION) .mp4'

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = f"""
    <html>
        <head>
            <title>Online cinema BLACKJACK</title>
            <style>
                body {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh; 
                    margin: 0; 
                    background-color: #f0f0f0; 
                }}
                h1 {{
                    margin-bottom: 20px; 
                }}
                video {{
                    max-width: 100%; 
                    height: auto; 
                }}
            </style>
        </head>
        <body>
            <h1>Welcome to BLACKJACK!</h1>
            <video controls>
                <source src="/video" type="video/mp4">
                Ваш браузер не поддерживает воспроизведение видео.
            </video>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)

@app.get("/video")
async def get_video():

    if os.path.exists(VIDEO_PATH):
        return FileResponse(VIDEO_PATH)
    return {"message": "Video file not found!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
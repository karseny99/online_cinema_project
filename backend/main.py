from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from fastapi.middleware.cors import CORSMiddleware
from handlers.user_handler import router as user_router
from handlers.movie_handler import router as movie_router

# from app.controllers.tag_controller import router as tag_router
# from app.controllers.rating_controller import router as rating_router

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname?sslmode=false"

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

@app.get("/")
async def root():
    return {"message": "Welcome to our online cinema!"}

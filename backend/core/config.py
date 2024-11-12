import os
from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    # DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL: str = "postgresql+asyncpg://pg-user:pg-password@localhost:5432/cinema-db"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "myjwtsecret")
    JWT_EXPIRATION_MINUTES: int = 30
    ALGORITHM: ClassVar[str] = "HS256"

settings = Settings()

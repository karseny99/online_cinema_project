import os
from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "myjwtsecret")
    JWT_EXPIRATION_MINUTES: int = 30
    ALGORITHM: ClassVar[str] = "HS256"

settings = Settings()

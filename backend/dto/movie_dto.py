from pydantic import BaseModel
from typing import List

class MovieDTO(BaseModel):
    id: int
    title: str
    genres: List[str]

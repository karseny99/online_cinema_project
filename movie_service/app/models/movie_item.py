from pydantic import BaseModel
from typing import Optional, List

'''
    Сейчас такой объект возвращает elastic search
'''
class MovieItem(BaseModel):
    movie_id: int
    movie_title: Optional[str]
    year: Optional[int]
    director: Optional[str]
    description: Optional[str]
    info_title: Optional[str]
    genres: List[Optional[str]]
    average_rating: Optional[float]
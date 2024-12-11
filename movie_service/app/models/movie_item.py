from pydantic import BaseModel, ValidationError
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
    genres: Optional[List[str]]
    average_rating: Optional[float]


'''
    Такое нужно кидать на вход функции elastic_search
'''
class SearchQueryElastic(BaseModel):
    title: Optional[str]
    year: Optional[int]
    genre: Optional[List[str]]  # <- я хз почему я не сделал множественное число как в возврате, но мне лень пиздец менять
    director: Optional[str]
    page: Optional[int]
    page_size: Optional[int]

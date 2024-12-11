from pydantic import BaseModel, ValidationError
from typing import Optional, List, Any


'''
    Внутренние классы сервиса и то, что будет лежать внутри body
    Для эластика сервис movie будет смотреть на contract_type: "search_request"
    Мейн будет ждать contract_type: "search_response"
'''

class ElasticRequest(BaseModel):
    title: Optional[str]
    year: Optional[int]
    genre: Optional[List[str]]  # <- я хз почему я не сделал множественное число как в возврате, но мне лень пиздец менять
    director: Optional[str]
    page: Optional[int]
    page_size: Optional[int]

class MovieItem(BaseModel):
    movie_id: int
    movie_title: Optional[str]
    year: Optional[int]
    director: Optional[str]
    description: Optional[str]
    info_title: Optional[str]
    genres: Optional[List[str]]
    average_rating: Optional[float]


class BaseContractModel(BaseModel):
    contract_type: str  # Поле для указания типа контракта
    body: Any


class ElasticResponse(BaseModel):
    movies: List[MovieItem]

class MovieInfoResponse(BaseModel):
    movie: MovieItem




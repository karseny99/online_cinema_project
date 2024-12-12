from datetime import date
from typing import Annotated

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import fastui_form
from pydantic import BaseModel, Field

API_URL = "http://localhost:8080"


def get_movies():
    response = requests.request("GET", API_URL + "/api/movies")
    return response


app = FastAPI()

c.Page.model_rebuild()


class Movie(BaseModel):
    id: int
    title: str = Field(title="Название")
    genres: str = Field(title="Жанры")


@app.get("/api/movies", response_model=FastUI, response_model_exclude_none=True)
def get_all_movies() -> list[AnyComponent]:
    # Получение списка фильмов
    movies = [Movie(**movie) for movie in get_movies().json()]
    print(movies)  # Для отладки

    # Генерация страницы с таблицей фильмов
    return [
        c.Page(
            components=[
                c.Heading(text='Фильмы', level=2),
                c.Table(
                    data=movies,  # Данные таблицы
                    data_model=Movie,  # Модель данных
                    columns=[
                        DisplayLookup(field='id'),
                        DisplayLookup(
                            field='title',
                            on_click=GoToEvent(url='/movies/{id}/')  # Ссылка с подстановкой id
                        ),
                    ],
                ),
            ]
        ),
    ]

@app.get("/api/movies/{movie_id}/", response_model=FastUI, response_model_exclude_none=True)
def movie_page(movie_id: int) -> list[AnyComponent]:
    movies = [Movie(**movie) for movie in get_movies().json()]
    for i in range(len(movies)):
        if i + 1 == movie_id:
            return [
                c.Page(
                    components=[
                        c.Heading(text=movies[i].title, level=2),
                        c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                        c.Details(data=movies[i]),
                    ]
                ),
            ]
    return [
        c.Page(
            components=[
                c.Heading(text='No film by such id')
            ]
        )
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Online cinema project'))

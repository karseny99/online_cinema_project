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
from typing import Optional, List
import uvicorn

API_URL = "http://localhost:8080"


def get_movies():
    response = requests.request("GET", API_URL + "/api/movies")
    return response


app = FastAPI()

c.Page.model_rebuild()


class Movie(BaseModel):
    movie_id: int
    movie_title: Optional[str]
    # year: Optional[int]
    # director: Optional[str]
    # description: Optional[str]
    # info_title: Optional[str]
    # genres: Optional[List[str]]
    # average_rating: Optional[float]


@app.get("/api/movies", response_model=FastUI, response_model_exclude_none=True)
def get_all_movies() -> list[AnyComponent]:
    # Получение списка фильмов
    # movies = [Movie(**movie) for movie in get_movies().json()]
    movies = [Movie(movie_title='Some title1', movie_id=1), Movie(movie_title='Some title2', movie_id=2)]
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
                        DisplayLookup(field='movie_id'),
                        DisplayLookup(
                            field='movie_title',
                            on_click=GoToEvent(url='/movies/{id}/')  # Ссылка с подстановкой id
                        ),
                    ],
                ),
            ]
        ),
    ]

@app.get("/api/movies/{movie_id}/", response_model=FastUI, response_model_exclude_none=True)
def movie_page(movie_id: int) -> list[AnyComponent]:
    # movies = [Movie(**movie) for movie in get_movies().json()]
    movie = Movie(movie_title='Some title', movie_id=1)
    print(f"MOVIE: {movie}")
    return [
        c.Page(
            components=[
                c.Heading(text=movie.movie_title, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=movie),
            ]
        ),
    ]
    # return [
    #     c.Page(
    #         components=[
    #             c.Heading(text='No film by such id')
    #         ]
    #     )
    # ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Online cinema project'))

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8081)

'''
c.Div(
            components=[
                c.Heading(text='Dynamic Modal', level=2),
                c.Markdown(
                    text=(
                        'The button below will open a modal with content loaded from the server when '
                        "it's opened using `ServerLoad`."
                    )
                ),
                c.Button(text='Show Dynamic Modal', on_click=PageEvent(name='dynamic-modal')),
                c.Modal(
                    title='Dynamic Modal',
                    body=[c.ServerLoad(path='/components/dynamic-content')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='dynamic-modal', clear=True)),
                    ],
                    open_trigger=PageEvent(name='dynamic-modal'),
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
'''
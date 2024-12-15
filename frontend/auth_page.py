import http

import requests
import json

from fastapi import FastAPI
from datetime import date
from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import fastui_form
from pydantic import BaseModel, EmailStr, constr, Field

API_BASE_URL = "http://localhost:8080"

session_token = {"access_token": None}

app = FastAPI()


def register_user_req(username, password, email, fullname) -> http.HTTPStatus:
    url = f"{API_BASE_URL}/auth/register"
    payload = {
        "request_id": "1234",
        "source": "fastui_client",
        "username": username,
        "password": password,
        "email": email,
        "full_name": fullname
    }
    response = requests.post(url, json=payload)
    return http.HTTPStatus(response.status_code)


def login_user_req(username, password) -> bool:
    url = f"{API_BASE_URL}/auth/login"
    payload = {
        "request_id": "1234",
        "source": "fastui_client",
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = json.loads(response.text)
        session_token["access_token"] = data["access_token"]
        return True
    else:
        return False


class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50) = Field(title="Логин")
    password: constr(min_length=8) = Field(title="Пароль")


class UserRegister(UserLogin):
    email: EmailStr = Field("Электронный адрес")
    full_name: Optional[str] = Field("ФИО")


c.Page.model_rebuild()
c.Modal.model_rebuild()

# @app.post("/api/user")
# def add_user(form: Annotated[UserAdd, fastui_form(UserAdd)]):
#     print(f"{form=}")
#     new_user = User(id=users[-1].id + 1 if users else 1, **form.model_dump())
#     users.append(new_user)
#     return [c.FireEvent(event=GoToEvent(url='/'))]


@app.post("/api/user/add", response_model=FastUI, response_model_exclude_none=True)
def add_user(form: Annotated[UserRegister, fastui_form(UserRegister)]):
    status = register_user_req(
        username=form.username,
        password=form.password,
        email=form.email,
        fullname=form.full_name,
    )

    if status == http.HTTPStatus.OK:
        print("User registered successfully!")
        return [
            c.Modal(
                title='Успешная регистрация',
                body=[c.Paragraph(text='Пользователь добавлен')],
                footer=[
                    c.Button(text='Close', on_click=PageEvent(name='static-modal', clear=True)),
                ],
                open_trigger=PageEvent(name='static-modal'),
            ),
            c.FireEvent(event=PageEvent(name='static-modal')),
            c.FireEvent(event=GoToEvent(url='/login'))
        ]
    elif status == http.HTTPStatus.BAD_REQUEST:
        return [c.FireEvent(event=GoToEvent(url='/register'))]


@app.post("/api/user/log-in")
def login_user(form: Annotated[UserLogin, fastui_form(UserLogin)]):
    try:
        success = login_user_req(
            username=form.username,
            password=form.password
        )
        if success:
            return [c.FireEvent(event=GoToEvent(url='/main_page'))]
        else:
            return [c.FireEvent(event=GoToEvent(url='/login'))]
    except Exception as e:
        print(f"Error occurred: {e}")


@app.get("/api/main_page", response_model=FastUI, response_model_exclude_none=True)
def show_main_page():
    return [
        c.Page(
            components=[
                c.Heading(text='Добро пожаловать в онлайн кинотеатр!'),
                c.Text(text="Online cinema")
            ]
        )
    ]


@app.get("/api/register", response_model=FastUI, response_model_exclude_none=True)
def add_user_page():
    return [
        c.Page(
            components=[
                c.Link(components=[c.Text(text='Назад')], on_click=BackEvent()),
                c.Heading(text='Зарегистрироваться', level=2),
                c.ModelForm(
                    model=UserRegister,
                    submit_url="/api/user/add"
                ),
            ]
        )
    ]


@app.get("/api/login", response_model=FastUI, response_model_exclude_none=True)
def login_user_page():
    return [
        c.Page(
            components=[
                c.Link(components=[c.Text(text='Назад')], on_click=BackEvent()),
                c.Heading(text='Вход', level=2),
                c.ModelForm(
                    model=UserLogin,
                    submit_url="/api/user/log-in"
                )
            ]
        )
    ]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text='Регистрация', level=2),
                c.Button(text="Зарегистрироваться", on_click=GoToEvent(url="/register")),
                c.Text(text="   или    "),
                c.Button(text="Войти", on_click=GoToEvent(url="/login"))
            ]
        ),
    ]


#
# @app.get("/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True)
# def user_profile(user_id: int) -> list[AnyComponent]:
#     try:
#         user = next(u for u in users if u.id == user_id)
#     except StopIteration:
#         raise HTTPException(status_code=404, detail="User not found")
#     return [
#         c.Page(
#             components=[
#                 c.Heading(text=user.name, level=2),
#                 c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
#                 c.Details(data=user),
#                 c.Button(text="Удалить пользователя", on_click=PageEvent(name="delete-user")),
#                 c.Form(
#                     submit_url="/api/user/delete",
#                     form_fields=[
#                         c.FormFieldInput(name='id', title='', initial=user_id, html_type='hidden')
#                     ],
#                     footer=[],
#                     submit_trigger=PageEvent(name="delete-user"),
#                 ),
#             ]
#         ),
#     ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Онлайн кинотеатр'))

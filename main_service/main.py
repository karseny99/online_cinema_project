from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from handlers.movie_handler import router as movie_router
from handlers.auth import router as auth_router
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="../frontend/templates")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(movie_router, prefix="/api", tags=["movies catalog"])
# TODO: other routes

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

# from models.movie_service_models import BaseContractModel, ElasticRequest
# from rpc_client.rpc_client import get_movie_rpc_client
# if __name__ == "__main__":
#     rpc_client = get_movie_rpc_client()
#     rpc_client.call(BaseContractModel("search_request", ElasticRequest()))
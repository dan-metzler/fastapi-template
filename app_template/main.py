from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/public"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/hello", response_class=HTMLResponse)
async def hello():
    return "<p class='notification is-success'>Hello from the server!</p>"

from typing import List, Dict

import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.model import Meteo


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_all_charts() -> List[Dict[str, str]]:
    charts = []
    for file in os.listdir("static/charts/"):
        if file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg"):
            filename = file.split(".")[0]
            file_info = {"name": filename, "href": file}
            charts.append(file_info)
    return charts


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    charts = get_all_charts()
    return templates.TemplateResponse(
        name="index.html", request=request, context={"charts": charts}
    )


@app.post("/upload/")
async def post(meteo: List[Meteo]) -> List[Meteo]:
    return meteo


@app.get("/chart/", response_class=HTMLResponse)
async def chart(
    request: Request,
    chart_name: str = "temperature",
) -> HTMLResponse:
    print(chart_name)
    return templates.TemplateResponse(
        name="chart.html", request=request, context={"chart": "test.gif"}
    )

from typing import List

import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.model import Requested_data

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_all_charts() -> List[str]:
    charts = []
    for file in os.listdir("static/charts/"):
        if file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg"):
            filename = file.split(".")[0]
            charts.append(filename)
    return charts


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    charts = get_all_charts()
    return templates.TemplateResponse(
        name="index.html", request=request, context={"charts": charts}
    )


@app.post("/upload/")
async def post(test: Requested_data) -> Requested_data:
    return test


@app.get("/chart/", response_class=HTMLResponse)
async def get_chart(
    request: Request,
    chart: str = "temperature",
) -> HTMLResponse:
    return templates.TemplateResponse(
        name="chart.html", request=request, context={"chart": chart}
    )

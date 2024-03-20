import os
from typing import List

from data_management.model import Meteo
from data_management.sql_commands import create_db, insert_data
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

if not os.path.exists("database/database.db"):
    create_db()

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
async def post(meteos: List[Meteo]) -> List[Meteo]:
    for item in meteos:
        try:
            item.model_validate(item)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors()) from exc
    insert_data(meteos)
    return meteos


@app.get("/chart/", response_class=HTMLResponse)
async def get_chart(
    request: Request,
    chart: str = "temperature",
) -> HTMLResponse:
    return templates.TemplateResponse(
        name="chart.html", request=request, context={"chart": chart}
    )


@app.get("/station/{station_id}", response_class=HTMLResponse)
async def get_station(request: Request, station_id: int) -> HTMLResponse:
    # get all the data for the station

    return templates.TemplateResponse(
        name="station.html", request=request, context={"station_id": station_id}
    )

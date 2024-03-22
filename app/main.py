from typing import List

from data_management.model import Meteo, Station
from data_management.sql_commands import (
    create_db,
    insert_data,
    get_all_stations,
    get_station_name,
)
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.functions import LIST_OF_GRAPH, get_all_charts_from_station, get_all_charts

create_db()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    stations = get_all_stations().to_dict(orient="records")
    print(stations)
    return templates.TemplateResponse(
        name="index.html", request=request, context={"stations": stations}
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


@app.post("/upload_station/")
async def post_station(stations: List[Station]) -> List[Station]:
    for station in stations:
        try:
            station.model_validate(station)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors()) from exc
    insert_data(stations)
    return stations


@app.get("/chart/{chart}", response_class=HTMLResponse)
async def get_chart(
    request: Request,
    chart: str,
) -> HTMLResponse:
    charts = get_all_charts(chart)
    title = LIST_OF_GRAPH[chart]["title"]
    return templates.TemplateResponse(
        name="chart.html", request=request, context={"charts": charts, "title": title}
    )


@app.get("/station/{station_id}", response_class=HTMLResponse)
async def get_station(request: Request, station_id: int) -> HTMLResponse:
    # get all the data for the station
    print(station_id)
    charts = get_all_charts_from_station(station_id)
    station_name = get_station_name(station_id)
    print(charts)
    return templates.TemplateResponse(
        name="station.html",
        request=request,
        context={"charts": charts, "station_name": station_name},
    )

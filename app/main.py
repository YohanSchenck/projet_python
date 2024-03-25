from typing import List

from data_management.model import Meteo, Station
from data_management.sql_commands import (
    create_db,
    insert_data,
    get_all_stations,
    get_station_name,
    get_top_hottest_year,
)
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.functions import (
    LIST_OF_GRAPH,
    get_all_charts_from_station,
    get_all_charts,
)

ENGINE = create_db()

APP = FastAPI()

APP.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")


@APP.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    stations = get_all_stations(ENGINE).to_dict(orient="records")
    return TEMPLATES.TemplateResponse(
        name="index.html", request=request, context={"stations": stations}
    )


@APP.post("/upload/")
async def post(meteos: List[Meteo]) -> List[Meteo]:
    for item in meteos:
        try:
            item.model_validate(item)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors()) from exc
    insert_data(meteos, ENGINE)
    return meteos


@APP.post("/upload_station/")
async def post_station(stations: List[Station]) -> List[Station]:
    for station in stations:
        try:
            station.model_validate(station)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors()) from exc
    insert_data(stations, ENGINE)
    return stations


@APP.get("/chart/{chart}", response_class=HTMLResponse)
async def get_chart(
    request: Request,
    chart: str,
) -> HTMLResponse:
    stations = get_all_stations(ENGINE).to_dict(orient="records")
    charts = get_all_charts(chart, stations)
    title = LIST_OF_GRAPH[chart]["title"]
    return TEMPLATES.TemplateResponse(
        name="chart.html", request=request, context={"charts": charts, "title": title}
    )


@APP.get("/station/{station_id}", response_class=HTMLResponse)
async def get_station(request: Request, station_id: int) -> HTMLResponse:
    # get all the data for the station
    charts = get_all_charts_from_station(station_id)
    station_name = get_station_name(station_id)
    return TEMPLATES.TemplateResponse(
        name="station.html",
        request=request,
        context={"charts": charts, "station_name": station_name},
    )


@APP.get("/top_hottest_year/{station_id}", response_class=HTMLResponse)
async def get_top_year(request: Request, station_id: int) -> HTMLResponse:
    years = get_top_hottest_year(ENGINE, station_id).to_dict(orient="records")
    station_name = get_station_name(station_id)
    return TEMPLATES.TemplateResponse(
        name="top_year.html",
        request=request,
        context={"years": years, "station_name": station_name},
    )

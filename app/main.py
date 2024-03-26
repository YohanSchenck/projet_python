import threading
from typing import List
import uvicorn
from data_management.model import Meteo, Station
from data_management.sql_commands import (
    create_db,
    insert_data,
    get_all_stations,
    get_station_name,
    get_top_hottest_year,
    get_unique_dates,
    verify_station,
    clear_station_table,
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
from moulinette.extract import monthly_dates_generator, request_meteo, process_meteo
from moulinette.upload import upload_meteo, upload_station
from data_management.graph import (
    create_graph_evol_temp,
    create_graph_wind,
    create_graph_temp_diff,
)
from moulinette.station import request_station, STATION_URL

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


@APP.post("/upload_meteo/")
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
    charts = get_all_charts_from_station(station_id)
    station_name = get_station_name(station_id, ENGINE)
    return TEMPLATES.TemplateResponse(
        name="station.html",
        request=request,
        context={"charts": charts, "station_name": station_name},
    )


@APP.get("/top_hottest_year/{station_id}", response_class=HTMLResponse)
async def get_top_year(request: Request, station_id: int) -> HTMLResponse:
    years = get_top_hottest_year(ENGINE, station_id).to_dict(orient="records")
    station_name = get_station_name(station_id, ENGINE)
    return TEMPLATES.TemplateResponse(
        name="top_year.html",
        request=request,
        context={"years": years, "station_name": station_name},
    )


if __name__ == "__main__":
    new_data = False
    host = "127.0.0.1"
    port = 8000
    webapp_thread = threading.Thread(
        name="Web App FastApi",
        daemon=True,
        target=uvicorn.run,
        args=(APP,),
        kwargs={"host": host, "port": port},
    )
    webapp_thread.start()
    if not verify_station(ENGINE):
        print("Station data is missing")
        print("Uploading station data ...")
        clear_station_table(ENGINE)
        upload_station(request_station(STATION_URL))

    dates = set(get_unique_dates(ENGINE)["date"])
    for monthly_date in monthly_dates_generator():
        print(f"Processing data for {monthly_date} ...")
        if monthly_date not in dates:
            new_data = True
            upload_meteo(process_meteo(request_meteo(monthly_date)))

    if new_data:
        print("New data has been uploaded")
        print("Generating charts ...")
        create_graph_evol_temp(ENGINE)
        create_graph_wind(ENGINE)
        create_graph_temp_diff(ENGINE)
        print("Charts have been generated")

    print(f"Webapp is running on http://{host}:{port} ...")
    try:
        while webapp_thread.is_alive():
            webapp_thread.join(1)
    except KeyboardInterrupt:
        print("Webapp has been stopped")

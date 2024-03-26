from concurrent.futures import ThreadPoolExecutor

import requests
import json

from moulinette.extract import (
    monthly_dates_generator,
    request_meteo,
    process_meteo,
)
from moulinette.station import request_station

POST_URL_METEO = "http://localhost:8000/upload_meteo/"
POST_URL_STATION = "http://localhost:8000/upload_station/"


def upload_meteo(data: str) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    send_data = json.loads(data)
    return requests.post(POST_URL_METEO, json=send_data, headers=headers, timeout=60)


def upload_station(data: str) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    send_data = json.loads(data)
    return requests.post(POST_URL_STATION, json=send_data, headers=headers, timeout=60)


def combinatoire(monthly_date: str) -> requests.Response:
    return upload_meteo(process_meteo(request_meteo(monthly_date)))


def main() -> None:
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(combinatoire, monthly_dates_generator())


if __name__ == "__main__":
    # for monthly_date in monthly_dates_generator(start="200001", end="200002"):
    #     print(f"Processing data for {monthly_date} ...")
    #     data = request_meteo(monthly_date)
    #     processed_data = process_meteo(data)
    #     response = upload_meteo(processed_data)
    station_data = request_station()
    upload_station(station_data)

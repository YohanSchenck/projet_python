import requests
import json

from moulinette.station import request_station, STATION_URL

POST_URL_METEO = "http://localhost:8000/upload/"
POST_URL_STATION = "http://localhost:8000/upload_station/"


def upload_meteo(data: str) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    send_data = json.loads(data)
    return requests.post(POST_URL_METEO, json=send_data, headers=headers, timeout=60)


def upload_station(data: str) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    send_data = json.loads(data)
    return requests.post(POST_URL_STATION, json=send_data, headers=headers, timeout=60)


if __name__ == "__main__":
    # for monthly_date in monthly_dates_generator(start="200001", end="200002"):
    #     print(f"Processing data for {monthly_date} ...")
    #     data = request_meteo(monthly_date)
    #     processed_data = process_meteo(data)
    #     response = upload_meteo(processed_data)
    station_data = request_station(STATION_URL)
    upload_station(station_data)

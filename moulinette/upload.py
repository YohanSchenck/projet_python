from concurrent.futures import ThreadPoolExecutor

import requests

from extract import monthly_dates_generator, request_data, process_data

POST_URL = "http://localhost:8000/upload/"


def upload_data(data: dict) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    return requests.post(POST_URL, data=data, headers=headers, timeout=15)


def combinatoire(monthly_date: str) -> requests.Response:
    return upload_data(process_data(request_data(monthly_date)))


def main() -> None:
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(combinatoire, monthly_dates_generator())


if __name__ == "__main__":
    for monthly_date in monthly_dates_generator():
        print(f"Processing data for {monthly_date} ...")
        data = request_data(monthly_date)
        print(type(data))

        processed_data = process_data(data)
        print(type(processed_data))

        response = upload_data(processed_data)
        print(response.status_code)
        break
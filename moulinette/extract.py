import gzip
from datetime import datetime

from typing import Iterator
import pandas as pd
import requests

BASE_URL = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.{date}.csv.gz"


def monthly_dates_generator(
    start: str = "199601", end: str = datetime.now().strftime("%Y%m")
) -> Iterator[str]:
    start_date = datetime.strptime(start, "%Y%m")
    end_date = datetime.strptime(end, "%Y%m")

    while start_date <= end_date:
        yield start_date.strftime("%Y%m")

        if start_date.month == 12:
            start_date = datetime(start_date.year + 1, 1, 1)
        else:
            start_date = datetime(start_date.year, start_date.month + 1, 1)


def request_data(request_date: str) -> pd.DataFrame:
    url = BASE_URL.format(date=request_date)

    try:
        data = pd.read_csv(url, sep=";", compression="gzip")
    except (gzip.BadGzipFile, requests.exceptions.RequestException) as error:
        print(f"Error while fetching data for {url}: {error}")
        return

    return data


def process_data(df: pd.DataFrame) -> dict:
    df.rename(
        columns={
            "numer_sta": "station_id",
            "ff": "wind",
            "t": "temperature",
        },
        inplace=True,
    )
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d%H%M%S", errors="coerce")

    df.loc[:, "year"] = df["date"].dt.year
    df.loc[:, "month"] = df["date"].dt.month
    df.loc[:, "week"] = df["date"].dt.isocalendar().week
    df.loc[:, "day"] = df["date"].dt.day
    df.loc[:, "hour"] = df["date"].dt.hour

    df.loc[:, "temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df.loc[:, "wind"] = pd.to_numeric(df["wind"], errors="coerce")

    df = df[
        ["station_id", "year", "month", "week", "day", "hour", "temperature", "wind"]
    ]

    df = df.dropna()

    df.loc[:, "temperature"] = df["temperature"] - 273.15
    return df.to_json(orient="records", lines=False)


if __name__ == "__main__":
    for monthly_date in monthly_dates_generator():
        print(f"Processing data for {monthly_date} ...")
        request_data(monthly_date)

        break

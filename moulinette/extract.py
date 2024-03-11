import gzip
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from io import BytesIO
from typing import Generator

import pandas as pd
import requests


def generate_monthly_dates_generator(
    start: str, end: str
) -> Generator[str, None, None]:
    start_date = datetime.strptime(start, "%Y%m")
    end_date = datetime.strptime(end, "%Y%m")

    while start_date <= end_date:
        yield start_date.strftime("%Y%m")
        if start_date.month == 12:
            start_date = datetime(start_date.year + 1, 1, 1)
        else:
            start_date = datetime(start_date.year, start_date.month + 1, 1)


json_folder = "./json"
base_url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop.{date}.csv.gz"
monthly_dates_generator = generate_monthly_dates_generator(
    "199601", datetime.now().strftime("%Y%m")
)


def process_date(date: str) -> None:
    url = base_url.format(date=date)
    json_filename = f"synop.{date}.json"

    response: requests.Response = requests.get(url)
    print(f"GET {url}")

    if response.status_code == 200:
        content = response.content
        try:
            with gzip.open(BytesIO(content), "rt", encoding="utf-8") as f_mem:
                df = pd.read_csv(f_mem, sep=";")
                df = df.rename(
                    columns={
                        "numer_sta": "station_id",
                        "ff": "wind",
                        "t": "temperature",
                    }
                )
                df["date"] = pd.to_datetime(df["date"], format="%Y%m%d%H%M%S")
                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month
                df["week"] = df["date"].dt.isocalendar().week
                df["day"] = df["date"].dt.day
                df["hour"] = df["date"].dt.hour
                df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
                df["temperature"].fillna(value=0, inplace=True)
                df["wind"] = pd.to_numeric(df["wind"], errors="coerce")
                df["wind"].fillna(value=0, inplace=True)
                df["temperature"] = df["temperature"] - 273.15
                df_clean = df[
                    [
                        "station_id",
                        "year",
                        "month",
                        "week",
                        "day",
                        "hour",
                        "wind",
                        "temperature",
                    ]
                ]
            if not os.path.exists(json_folder):
                os.makedirs(json_folder)
            json_path = os.path.join(json_folder, json_filename)
            df_clean.to_json(json_path, orient="records", lines=True)
            print(f"Fichier {json_filename} enregistré dans le dossier {json_folder}.")
        except gzip.BadGzipFile:
            print("Le contenu téléchargé n'est pas un fichier gzip valide.")
    else:
        print(f"Url : {url} ne répond pas, vérifiez l'url fourni ou l'état du serveur.")


with ThreadPoolExecutor(max_workers=128) as executor:
    executor.map(process_date, monthly_dates_generator)

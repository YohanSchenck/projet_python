import os

import matplotlib.pyplot as plt
from pandas import to_datetime

from sql_commands import get_evolution_temp, get_evolution_wind


def create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def create_graph_evol_temp() -> None:
    df = get_evolution_temp()
    df["date"] = to_datetime(df["year"] * 1000 + df["day"], format="%Y%j")

    list_station = df["station_id"].unique()

    create_dir("static/charts/evolution_temperature/")

    for station in list_station:
        df_station = df[df["station_id"] == station].sort_values(by=["date"])
        df_station["avg_temp"] = df_station["avg_temp"].rolling(365).mean()
        df_station.plot(kind="line", x="date", y="avg_temp", figsize=(20, 10))
        plt.grid()
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
        plt.gca().legend().remove()
        plt.savefig(f"static/charts/evolution_temperature/{station}.png")
        plt.close()


def create_graph_wind() -> None:
    df = get_evolution_wind()
    wind_force = 4.16
    df = df[df["avg_wind"] <= wind_force].sort_values(by=["year"])
    list_station = df["station_id"].unique()

    create_dir("static/charts/evolution_wind/")

    for station in list_station:
        df_station = df[df["station_id"] == station]
        df_station = (
            df_station[["year", "avg_wind"]].groupby(["year"], as_index=False).count()
        )
        df_station.plot(kind="bar", x="year", y="avg_wind", figsize=(20, 10))
        plt.grid()
        plt.gca().legend().remove()
        plt.savefig(f"static/charts/evolution_wind/{station}.png")
        plt.close()


# create_graph_evol_temp()
create_graph_wind()

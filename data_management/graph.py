import os

import matplotlib.pyplot as plt
from pandas import DataFrame, to_datetime

from data_management.sql_commands import (
    get_all_stations,
    get_evolution_temp,
    get_evolution_temp_from_station,
    get_evolution_wind,
)


def get_top_hottest_year() -> DataFrame:
    df = get_evolution_temp()
    df_hottest_year = df[["year", "avg_temp"]].groupby(["year"], as_index=False).mean()
    df_hottest_year = df_hottest_year.nlargest(10, "avg_temp").sort_values(
        by=["avg_temp"], ascending=False
    )
    return df_hottest_year


def create_graph_evol_temp() -> None:
    os.makedirs("static/charts/evolution_temperature/", exist_ok=True)

    list_station = get_all_stations()["station_id"].values

    for station in list_station:
        df_station = get_evolution_temp_from_station(station_id=station)
        df_station["date"] = to_datetime(
            df_station["year"] * 1000 + df_station["day"], format="%Y%j"
        )
        df_station = df_station.sort_values(by=["date"])
        df_station["avg_temp"] = df_station["avg_temp"].rolling(365).mean()
        df_station.plot(kind="line", x="date", y="avg_temp", figsize=(20, 10))
        plt.grid()
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
        plt.gca().legend().remove()
        plt.savefig(f"static/charts/evolution_temperature/{station}.png")
        plt.close()


def create_graph_wind() -> None:
    os.makedirs("static/charts/evolution_wind/", exist_ok=True)
    wind_force = 4.16
    list_station = get_all_stations()["station_id"].values

    for station in list_station:
        df_station = get_evolution_wind(station)
        list_year = df_station["year"].unique()
        df_station = df_station[df_station["avg_wind"] <= wind_force]
        df_station = (
            df_station[["year", "avg_wind"]].groupby(["year"], as_index=False).count()
        )
        for year in list_year:
            if year not in df_station["year"].unique():
                df_station.loc[len(df_station.index)] = [year, 0]

        df_station = df_station.sort_values(by=["year"])

        df_station.plot(kind="bar", x="year", y="avg_wind", figsize=(20, 10))
        plt.grid()
        plt.gca().legend().remove()
        plt.savefig(f"static/charts/evolution_wind/{station}.png")
        plt.close()


if __name__ == "__main__":
    create_graph_evol_temp()
    create_graph_wind()

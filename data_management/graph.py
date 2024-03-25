import os

import matplotlib.pyplot as plt
from pandas import DataFrame, to_datetime
from sqlalchemy import Engine

from data_management.sql_commands import (
    get_all_stations,
    get_evolution_diff_temperature,
    get_evolution_temp,
    get_evolution_temp_from_station,
    get_evolution_wind,
)


def get_top_hottest_year(engine: Engine) -> DataFrame:
    """
    Get the top 10 hottest year

    Parameters
    ----------

    Returns
    -------
    Dataframe containing the data structured (year,avg_temp)
    """
    df = get_evolution_temp(engine=engine)
    df_hottest_year = df[["year", "avg_temp"]].groupby(["year"], as_index=False).mean()
    df_hottest_year = df_hottest_year.nlargest(10, "avg_temp").sort_values(
        by=["avg_temp"], ascending=False
    )
    return df_hottest_year


def create_graph_evol_temp(engine: Engine) -> None:
    """
    Create all graphs observing the evolution of temperature

    Parameters
    ----------
    engine : engine database

    Returns
    -------
    """

    os.makedirs("static/charts/evolution_temperature/", exist_ok=True)

    list_station = get_all_stations(engine=engine)["station_id"].values

    for station in list_station:
        df_station = get_evolution_temp_from_station(station_id=station, engine=engine)
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


def create_graph_wind(engine: Engine) -> None:
    """
    Create all graphs observing the number of days where the wind turbine can't work

    Parameters
    ----------
    engine : engine database

    Returns
    -------
    """
    os.makedirs("static/charts/evolution_wind/", exist_ok=True)
    wind_force = 4.16
    list_station = get_all_stations(engine=engine)["station_id"].values

    for station in list_station:
        df_station = get_evolution_wind(station, engine=engine)
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


def create_graph_temp_diff(engine: Engine) -> None:
    """
    Create all graphs observing the difference of temperature between 1996 and today

    Parameters
    ----------
    engine : engine database

    Returns
    -------
    """

    os.makedirs("static/charts/difference_temperature/", exist_ok=True)

    list_station = get_all_stations(engine)["station_id"].values

    for station in list_station:
        df_station = get_evolution_diff_temperature(station_id=station, engine=engine)
        df_station["date"] = to_datetime(
            df_station["year"] * 1000 + df_station["day"], format="%Y%j"
        )
        df_station = df_station.sort_values(by=["date"])
        df_station.plot(kind="line", x="date", y="difference", figsize=(40, 15))
        plt.grid()
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())
        plt.gca().legend().remove()
        plt.savefig(f"static/charts/difference_temperature/{station}.png")
        plt.close()


# create_graph_evol_temp()
# create_graph_wind()
# create_graph_temp_diff()

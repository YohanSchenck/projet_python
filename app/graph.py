import matplotlib.pyplot as plt
from pandas import DataFrame
from sql_commands import (
    get_evolution_temp,
    get_evolution_wind,
)
# df = read_csv("../données_evol_temp.csv", delimiter=";")
# df_wind = read_csv("../données_wind.csv", delimiter=";")


def create_graph_evol_temp() -> None:
    df = get_evolution_temp()
    list_station = df["station_id"].unique()

    for station in list_station:
        df_station = df[df["station_id"] == station].sort_values(by=["year"])
        df_station.plot(kind="line", x="year", y="avg_temp")
        plt.xticks(range(df_station["year"].min(), df_station["year"].max() + 1))
        plt.grid()
        plt.savefig(f"static/charts/evol_temp_{station}.png")
        plt.close()


def create_graph_wind(df: DataFrame) -> None:
    df = get_evolution_wind()
    wind_force = 4.16
    df = df[df["avg_wind"] <= wind_force].sort_values(by=["year"])
    list_station = df["station_id"].unique()

    for station in list_station:
        df_station = df[df["station_id"] == station]
        df_station = (
            df_station[["year", "avg_wind"]].groupby(["year"], as_index=False).count()
        )
        df_station.plot(kind="bar", x="year", y="avg_wind")
        print(range(df_station["year"].min(), df_station["year"].max() + 1))
        plt.yticks(
            range(df_station["avg_wind"].min(), df_station["avg_wind"].max() + 1)
        )
        plt.grid()
        plt.savefig(f"static/charts/evol_wind_{station}.png")
        plt.close()


create_graph_evol_temp()
# create_graph_wind()

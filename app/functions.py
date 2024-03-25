from typing import List, Dict
import os
from data_management.sql_commands import get_all_stations

LIST_OF_GRAPH = {
    "evolution_temperature": {
        "path": "evolution_temperature",
        "title": "Evolution de la température (moyenne glissante sur 1 an)",
    },
    "evolution_wind": {
        "path": "evolution_wind",
        "title": "Nombre de jours où les éoliennes n'ont pas pu fonctionner",
    },
}


def get_all_charts_from_station(station_id: int) -> List[Dict[str, str]]:
    """
    Get all the charts from a station

    Parameters
    ----------
    station_id : id station

    Returns
    -------
    List of all the charts from a station
    """
    charts = []
    for key in LIST_OF_GRAPH:
        if os.path.exists(
            f"static/charts/{LIST_OF_GRAPH[key]["path"]}/{station_id}.png"
        ):
            charts.append(
                {
                    **LIST_OF_GRAPH[key],
                    "path": f"{LIST_OF_GRAPH[key]['path']}/{station_id}.png",
                }
            )
    return charts


def get_all_charts(chart: str) -> List[Dict[str, str]]:
    """
    Get all the charts

    Parameters
    ----------

    Returns
    -------
    List of all the charts
    """
    stations = get_all_stations()
    charts = []
    for station in stations.to_dict(orient="records"):
        if os.path.exists(f"static/charts/{chart}/{station['station_id']}.png"):
            charts.append(
                {
                    "station_name": station["station_name"],
                    "path": f"{chart}/{station['station_id']}.png",
                }
            )

    return charts

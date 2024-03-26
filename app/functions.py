from typing import List, Dict
import os

LIST_OF_GRAPH = {
    "evolution_temperature": {
        "path": "evolution_temperature",
        "title": "Evolution de la température (moyenne glissante sur 1 an)",
    },
    "evolution_wind": {
        "path": "evolution_wind",
        "title": "Nombre de jours où les éoliennes n'ont pas pu fonctionner",
    },
    "difference_temperature": {
        "path": "difference_temperature",
        "title": "Ecart maximum de température par semaine",
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


def get_all_charts(chart: str, stations: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Get all the charts

    Parameters
    ----------

    Returns
    -------
    List of all the charts
    """
    charts = []
    for station in stations:
        if os.path.exists(f"static/charts/{chart}/{station['station_id']}.png"):
            charts.append(
                {
                    "station_name": station["station_name"],
                    "path": f"{chart}/{station['station_id']}.png",
                }
            )

    return charts

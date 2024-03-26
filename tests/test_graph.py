import os
from typing import List

import pytest
from data_management.graph import (
    create_graph_evol_temp,
    create_graph_temp_diff,
    create_graph_wind,
)
from data_management.model import Meteo, Station
from data_management.sql_commands import get_engine, insert_data, get_top_hottest_year
from sqlalchemy import Engine
from sqlmodel import SQLModel


@pytest.fixture
def init_database() -> Engine:
    path: str = ":memory:"
    engine = get_engine(path)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def create_3_Meteo() -> List[Meteo]:
    data: List[Meteo] = []

    meteo1 = Meteo(
        station_id=102,
        year=2024,
        month=1,
        week=1,
        day=1,
        hour=9,
        wind=20.5,
        temperature=10.3,
    )

    meteo2 = Meteo(
        station_id=102,
        year=2024,
        month=1,
        week=1,
        day=2,
        hour=9,
        wind=20.5,
        temperature=20.3,
    )

    meteo3 = Meteo(
        station_id=103,
        year=2023,
        month=1,
        week=1,
        day=1,
        hour=9,
        wind=20.5,
        temperature=10.3,
    )

    data.append(meteo1)
    data.append(meteo2)
    data.append(meteo3)
    return data


@pytest.fixture
def create_2_Station() -> List[Station]:
    data: List[Station] = []

    station1 = Station(station_id=102, station_name="Bordeaux")

    station2 = Station(station_id=103, station_name="Paris")

    data.append(station1)
    data.append(station2)
    return data


def test_create_graph_evol_temp(
    init_database, create_3_Meteo, create_2_Station
) -> None:
    meteos = create_3_Meteo
    stations = create_2_Station

    engine = init_database

    insert_data(meteos, engine=engine)
    insert_data(stations, engine=engine)

    create_graph_evol_temp(engine=engine)

    assert (os.path.isfile("static/charts/evolution_temperature/103.png")) is True
    assert (os.path.isfile("static/charts/evolution_temperature/102.png")) is True

    os.remove("static/charts/evolution_temperature/103.png")
    os.remove("static/charts/evolution_temperature/102.png")


def test_create_graph_temp_diff(
    init_database, create_3_Meteo, create_2_Station
) -> None:
    meteos = create_3_Meteo
    stations = create_2_Station

    engine = init_database

    insert_data(meteos, engine=engine)
    insert_data(stations, engine=engine)

    create_graph_temp_diff(engine=engine)

    assert (os.path.isfile("static/charts/difference_temperature/103.png")) is True
    assert (os.path.isfile("static/charts/difference_temperature/102.png")) is True

    os.remove("static/charts/difference_temperature/103.png")
    os.remove("static/charts/difference_temperature/102.png")


def test_create_graph_wind(init_database, create_3_Meteo, create_2_Station) -> None:
    meteos = create_3_Meteo
    stations = create_2_Station

    engine = init_database

    insert_data(meteos, engine=engine)
    insert_data(stations, engine=engine)

    create_graph_wind(engine=engine)

    assert (os.path.isfile("static/charts/evolution_wind/103.png")) is True
    assert (os.path.isfile("static/charts/evolution_wind/102.png")) is True

    os.remove("static/charts/evolution_wind/103.png")
    os.remove("static/charts/evolution_wind/102.png")


def test_create_get_top_hottest_year(init_database, create_3_Meteo) -> None:
    meteos = create_3_Meteo

    engine = init_database

    insert_data(meteos, engine=engine)

    df = get_top_hottest_year(engine, 102)

    assert (len(df)) == 1
    assert (len(df.columns)) == 2

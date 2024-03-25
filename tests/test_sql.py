import os
from typing import List

import pytest
from data_management.model import Meteo, Station
from data_management.sql_commands import (
    create_db,
    get_engine,
    get_evolution_diff_temperature,
    get_evolution_wind,
    get_station_name,
    insert_data,
    verify_availibity_meteo,
)
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, select


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
        station_id=102,
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


def test_insert_data(init_database, create_3_Meteo) -> None:
    data = create_3_Meteo

    engine = init_database

    insert_data(data, engine=engine)

    with Session(engine) as session:
        statement = select(Meteo)
        result = session.exec(statement).all()
        assert (result[0].station_id) == 102
        assert (result[0].year) == 2024
        assert (result[0].month) == 1
        assert (result[0].day) == 1
        assert (result[0].wind) == 20.5
        assert (result[0].temperature) == 10.3


def test_create_database() -> None:
    create_db()
    assert (os.path.isfile("database/database.db")) is True


def test_get_evolution_wind(init_database, create_3_Meteo) -> None:
    data = create_3_Meteo
    engine = init_database
    insert_data(data, engine)

    df = get_evolution_wind(station_id=102, engine=engine)

    assert (len(df)) == 3
    assert (len(df.columns)) == 3


def test_get_evolution_diff_temperature(init_database, create_3_Meteo) -> None:
    data = create_3_Meteo
    engine = init_database
    insert_data(data, engine)

    df = get_evolution_diff_temperature(station_id=102, engine=engine)

    assert (len(df)) == 2
    assert (len(df.columns)) == 4


def test_get_station_name(init_database, create_2_Station):
    data = create_2_Station
    engine = init_database
    insert_data(data, engine)

    assert (get_station_name(102, engine)) == "Bordeaux"


def test_verify_availibity_meteo(init_database, create_3_Meteo) -> None:
    data = create_3_Meteo
    engine = init_database
    insert_data(data, engine)

    assert (verify_availibity_meteo("2024", "1", engine=engine)) == True
    assert (verify_availibity_meteo("2027", "1", engine=engine)) == False

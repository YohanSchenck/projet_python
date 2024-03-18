import os
from typing import List

import pytest
from app.model import Meteo
from app.sql import (
    create_db,
    get_evolution_diff_temperature,
    get_evolution_temp,
    get_evolution_wind,
    insert_data,
)
from sqlmodel import Session, SQLModel, create_engine, select


@pytest.fixture
def init_database():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def create_2_Meteo():
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


def test_insert_data(init_database, create_2_Meteo) -> None:
    data = create_2_Meteo

    engine = init_database

    insert_data(engine, data)

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
    assert (os.path.isfile("database.db")) is True


def test_get_evolution_temp(init_database, create_2_Meteo) -> None:
    data = create_2_Meteo
    engine = init_database
    insert_data(engine, data)

    df = get_evolution_temp(engine)

    assert (len(df)) == 2
    assert (len(df.columns)) == 3


def test_get_evolution_wind(init_database, create_2_Meteo) -> None:
    data = create_2_Meteo
    engine = init_database
    insert_data(engine, data)

    df = get_evolution_wind(engine)

    assert (len(df)) == 3
    assert (len(df.columns)) == 4


def test_get_evolution_diff_temperature(init_database, create_2_Meteo) -> None:
    data = create_2_Meteo
    engine = init_database
    insert_data(engine, data)

    df = get_evolution_diff_temperature(engine)

    assert (len(df)) == 2
    assert (len(df.columns)) == 4

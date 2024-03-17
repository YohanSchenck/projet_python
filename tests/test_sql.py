from datetime import datetime
from typing import List

import pytest
from app.model import Meteo
from app.sql import insert_data
from sqlmodel import Session, SQLModel, create_engine, select


@pytest.fixture
def init_database():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


def test_insert_data(init_database) -> None:
    data: List[Meteo] = []
    date = datetime.now()

    engine = init_database

    meteo1 = Meteo(
        station_id=102,
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        wind=20.5,
        temperature=10.3,
    )
    data.append(meteo1)

    insert_data(engine, data)

    with Session(engine) as session:
        statement = select(Meteo)
        result = session.exec(statement).all()
        assert (result[0].station_id) == 102
        assert (result[0].year) == 2024
        assert (result[0].month) == 3
        assert (result[0].day) == 11
        assert (result[0].wind) == 20.5
        assert (result[0].temperature) == 10.3

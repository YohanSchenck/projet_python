from datetime import datetime
from typing import Any, List

from sqlmodel import Session, SQLModel, create_engine

from model import Meteo

engine = create_engine("sqlite:///database.db", echo=True)


def create_database(engine: Any) -> None:
    """
    Create the file database.db

    Parameters
    ----------
    engine : database

    Returns
    -------
    """
    SQLModel.metadata.create_all(engine)


date = datetime.now()

meteo1 = Meteo(
    station_id=102,
    year=date.year,
    month=date.month,
    day=date.day,
    hour=date.hour,
    wind=20.5,
    temperature=10.3,
)
meteo2 = Meteo(
    station_id=123,
    year=date.year,
    month=date.month,
    day=date.day,
    hour=date.hour,
    wind=23.5,
    temperature=10.3,
)

data: List[Meteo] = []

data.append(meteo1)
data.append(meteo2)

# print(data)


def insert_data(engine: Any, data: List[Meteo]) -> None:
    """
    Insert the list of data into the database

    Parameters
    ----------
    engine : database

    data : list of data. Type can be the different models

    Returns
    -------
    """
    with Session(engine) as session:
        for row in data:
            session.add(row)

        session.commit()


create_database(engine)
insert_data(engine, data)

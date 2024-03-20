from typing import List

from pandas import DataFrame, read_sql_query
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.model import Meteo


def get_engine() -> Engine:
    """
    Get the database engine

    Parameters
    ----------

    Returns
    -------
    Engine : database engine
    """
    return create_engine("sqlite:///database/database.db", echo=True)


def create_db() -> None:
    """
    Create Database

    Parameters
    ----------

    Returns
    -------
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def insert_data(data: List[Meteo]) -> None:
    """
    Insert the list of data into the database

    Parameters
    ----------
    engine : database

    data : list of data.

    Returns
    -------
    """

    with Session(get_engine()) as session:
        for row in data:
            session.add(row)

        session.commit()


def get_evolution_temp() -> DataFrame:
    """
    Get the evolution of temperature

    Parameters
    ----------


    Returns
    -------
    Dataframe containing the data structured (station_id, year, avg_temp)
    """
    with get_engine().connect() as con:
        df = read_sql_query(
            "SELECT station_id, year, day, AVG(temperature) as avg_temp from Meteo GROUP BY station_id, year, day",
            con,
        )
    return df


def get_evolution_wind() -> DataFrame:
    """
    Get the evolution of wind

    Parameters
    ----------


    Returns
    -------
    Dataframe containing the data structured (station_id, year,day avg_wind)
    """
    with get_engine().connect() as con:
        df = read_sql_query(
            "SELECT station_id, year,day, AVG(wind) as avg_wind from Meteo GROUP BY station_id, year, day",
            con,
        )
    return df


def get_evolution_diff_temperature() -> DataFrame:
    """
    Get the evolution of the temperature difference

    Parameters
    ----------

    Returns
    -------
    Dataframe containing the data structured (station_id, year,week,  diff_temp)
    """
    with get_engine().connect() as con:
        df = read_sql_query(
            "SELECT station_id, year, week, (MAX(temperature) - MIN(temperature)) as difference from Meteo GROUP BY station_id, year, week",
            con,
        )
    return df

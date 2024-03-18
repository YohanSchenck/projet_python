from typing import Any, List

from pandas import DataFrame, read_sql_query
from sqlmodel import Session, SQLModel, create_engine

from app.model import Meteo


def create_db() -> None:
    """
    Create Database

    Parameters
    ----------

    Returns
    -------
    """
    engine = create_engine("sqlite:///database.db", echo=True)
    SQLModel.metadata.create_all(engine)


def insert_data(engine: Any, data: List[Meteo]) -> None:
    """
    Insert the list of data into the database

    Parameters
    ----------
    engine : database

    data : list of data.

    Returns
    -------
    """

    with Session(engine) as session:
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

    engine = create_engine("sqlite:///database.db", echo=True)
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT station_id, year, AVG(temperature) from Meteo GROUP BY station_id, year",
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
    engine = create_engine("sqlite:///database.db", echo=True)
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT station_id, year,day, AVG(wind) from Meteo GROUP BY station_id, year, day",
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
    Dataframe containing the data structured (station_id, year,week,  diff_wind)
    """
    engine = create_engine("sqlite:///database.db", echo=True)
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT station_id, year, week, (MAX(temperature) - MIN(temperature)) as difference from Meteo GROUP BY station_id, year, week",
            con,
        )
    return df

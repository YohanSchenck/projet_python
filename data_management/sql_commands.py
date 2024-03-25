from typing import List

from pandas import DataFrame, read_sql_query
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from data_management.model import Meteo, Station


def get_engine(path: str = "database/database.db") -> Engine:
    """
    Get the database engine

    Parameters
    ----------
    path : Path of database has to be defined in case of test

    Returns
    -------
    Engine : database engine
    """
    return create_engine(f"sqlite:///{path}")


def create_db() -> Engine:
    """
    Create Database

    Parameters
    ----------

    Returns
    -------
    Engine : database engine with tables created
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    return engine


def insert_data(data: List[Station] | List[Meteo], engine: Engine) -> None:
    """
    Insert the list of data into the database

    Parameters
    ----------
    data : list of data.

    path : Path of database has to be defined in case of test

    Returns
    -------
    """

    with Session(engine) as session:
        for row in data:
            session.add(row)

        session.commit()


def get_evolution_temp_from_station(station_id: int, engine: Engine) -> DataFrame:
    """
    Get the evolution of temperature from a specific id

    Parameters
    ----------
    station_id : id station

    path : Path of database has to be defined in case of test

    Returns
    -------
    Dataframe containing the data structured (year, avg_temp)
    """
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT year, day, AVG(temperature) as avg_temp from Meteo WHERE station_id = :station GROUP BY year, day",
            con,
            params={"station": str(station_id)},
        )
    return df


def get_all_stations(engine: Engine) -> DataFrame:
    """
    Get all stations

    Parameters
    ----------

    path : Path of database has to be defined in case of test

    Returns
    -------
    Dataframe containing a list of all stations
    """
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT station_id, station_name from Station",
            con,
        )
    return df


def get_evolution_wind(station_id: int, engine: Engine) -> DataFrame:
    """
    Get the evolution of wind

    Parameters
    ----------
    station_id : id station

    path : Path of database has to be defined in case of test

    Returns
    -------
    Dataframe containing the data structured (year,day, avg_wind)
    """
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT year,day, AVG(wind) as avg_wind from Meteo WHERE station_id = :station GROUP BY year, day",
            con,
            params={"station": str(station_id)},
        )
    return df


def get_evolution_diff_temperature(station_id: int, engine: Engine) -> DataFrame:
    """
    Get the evolution of the temperature difference from station id

    Parameters
    ----------
    station_id : id station

    path : Path of database has to be defined in case of test

    Returns
    -------
    Dataframe containing the data structured (year,week,  diff_temp)
    """
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT year, week, MIN(day) as day, (MAX(temperature) - MIN(temperature)) as difference from Meteo WHERE station_id = :station GROUP BY year, week",
            con,
            params={"station": str(station_id)},
        )
    return df


def get_station_name(station_id: int, engine: Engine) -> str:
    """
    Get the name of the station

    Parameters
    ----------
    station_id : id station

    Returns
    -------
    Name of the station
    """
    with engine.connect() as con:
        df = read_sql_query(
            "SELECT station_name from Station WHERE station_id = :station",
            con,
            params={"station": str(station_id)},
        )
    return df["station_name"].values[0]


def get_top_hottest_year(engine: Engine, station: int) -> DataFrame:
    """
    Get the top 10 hottest year

    Parameters
    ----------
    engine : engine database

    Returns
    -------
    Dataframe containing the data structured (year,avg_temp)
    """
    df = get_evolution_temp_from_station(station, engine=engine)
    df_hottest_year = df[["year", "avg_temp"]].groupby(["year"], as_index=False).mean()
    df_hottest_year = df_hottest_year.nlargest(10, "avg_temp").sort_values(
        by=["avg_temp"], ascending=False
    )
    df_hottest_year["avg_temp"] = df_hottest_year["avg_temp"].round(3)
    return df_hottest_year

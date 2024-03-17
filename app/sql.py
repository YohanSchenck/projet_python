from typing import Any, List

from pandas import DataFrame
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

    engine = create_engine("sqlite:///:memory:", echo=True)
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
    # con = sqlite3.connect("data/portal_mammals.sqlite")
    # df = pd.read_sql_query("SELECT * from surveys", con)

    # Verify that result of SQL query is stored in the dataframe
    # print(df.head())

    # con.close()
    return DataFrame

from typing import Any, List

from sqlmodel import Session, SQLModel, create_engine

from app.model import Meteo

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

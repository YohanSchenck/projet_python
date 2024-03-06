from typing import Any, List

from app.sql import create_database
from sqlalchemy import Engine, create_engine, inspect, types


def test_create_database() -> None:
    queries: List[Any] = ["CREATE TABLE Test (date date,ID int, temp decimal)"]

    engine: Engine = create_engine("sqlite:///:memory:", echo=True)

    create_database(engine, queries)

    assert (inspect(engine).get_table_names()[0]) == "Test"
    assert (inspect(engine).get_columns("Test")[0].get("name")) == "date"
    assert (type(inspect(engine).get_columns("Test")[0].get("type"))) == types.DATE
    assert (inspect(engine).get_columns("Test")[1].get("name")) == "ID"
    assert (type(inspect(engine).get_columns("Test")[1].get("type"))) == types.INT
    assert (inspect(engine).get_columns("Test")[2].get("name")) == "temp"
    assert (type(inspect(engine).get_columns("Test")[2].get("type"))) == types.DECIMAL

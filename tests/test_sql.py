import sqlalchemy
from app import create_database


def test_create_database():
    queries = ["CREATE TABLE Test (date date,ID int, temp decimal)"]

    engine = sqlalchemy.create_engine("sqlite:///test.db", echo=True)

    create_database(engine, queries)

    assert (sqlalchemy.inspect(engine).get_table_names()[0]) == "Test"

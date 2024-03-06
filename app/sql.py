import sqlalchemy
from sqlalchemy import Engine, create_engine, text

engine = create_engine("sqlite:///database.db", echo=True)

list_query = [
    "CREATE TABLE Donnees_brutes (date date,ID_Station int, temp decimal, vent decimal)",
    "CREATE TABLE Evolution_temp (annee int, ID_Station int, temp decimal)",
    "CREATE TABLE Evolution_vent (annee int, jour int, ID_Station int, vent decimal)",
    "CREATE TABLE Ecart_temp (annee int, semaine int, ID_Station int, ecart_temp decimal)",
]


def create_database(engine: Engine, list_query: list):
    with engine.connect() as conn:
        for query in list_query:
            conn.execute(text(query))


# create_database(engine, list_query)


print(sqlalchemy.inspect(engine).get_table_names()[0])

# print(sqlalchemy.inspect(engine).get_columns("Donnees_brutes"))

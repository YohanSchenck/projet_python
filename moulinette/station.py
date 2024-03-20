import pandas as pd

STATION_URL = (
    "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/postesSynop.csv"
)


def get_station_data() -> str:
    try:
        data = pd.read_csv(STATION_URL, sep=";")
    except pd.errors.ParserError as error:
        print(f"Error while fetching data for {STATION_URL}: {error}")
        raise error
    data.rename(columns={"ID": "station_id", "Nom": "station_name"}, inplace=True)
    data.drop(columns=["Latitude", "Longitude", "Altitude"], inplace=True)
    return data.to_json(orient="records")

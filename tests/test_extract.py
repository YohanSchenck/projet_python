from unittest.mock import patch, MagicMock
from moulinette.extract import monthly_dates_generator, request_data, process_data
import pandas as pd
import gzip
import requests


def test_monthly_dates_generator_change_year() -> None:
    dates = list(monthly_dates_generator("202112", "202202"))
    assert dates == [
        "202112",
        "202201",
        "202202",
    ], "The generator should correctly handle the transition from December to January."


def test_request_data_success() -> None:
    with patch("pandas.read_csv") as mock_read_csv:
        mock_df = MagicMock(spec=pd.DataFrame)
        mock_read_csv.return_value = mock_df
        df = request_data("202001")
        assert df is mock_df


def test_request_data_exceptions() -> None:
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.side_effect = requests.exceptions.RequestException
        df = request_data("202001")
        assert df is None

        mock_read_csv.side_effect = gzip.BadGzipFile
        df = request_data("202001")
        assert df is None


def test_process_data_column_renaming() -> None:
    raw_data = {
        "numer_sta": [12345],
        "ff": [10.0],
        "t": [293.15],
        "date": ["20200101120000"],
    }
    test_df = pd.DataFrame(raw_data)
    processed_json = process_data(test_df)
    processed_df = pd.read_json(processed_json)

    expected_columns = [
        "station_id",
        "year",
        "month",
        "week",
        "day",
        "hour",
        "temperature",
        "wind",
    ]
    assert (
        list(processed_df.columns) == expected_columns
    ), "Column names should be renamed correctly."


def test_process_data_temperature_conversion() -> None:
    raw_data = {
        "numer_sta": [12345],
        "ff": [10.0],
        "t": [273.15],  # 0°C
        "date": ["20200101120000"],
    }
    test_df = pd.DataFrame(raw_data)
    processed_json = process_data(test_df)
    processed_df = pd.read_json(processed_json)

    assert (
        processed_df["temperature"][0] == 0
    ), "Temperature should be converted to Celsius."


def test_process_data_dropna() -> None:
    raw_data = {
        "numer_sta": [12345, None],
        "ff": [10.0, 20.0],
        "t": [273.15, None],
        "date": ["20200101120000", None],
    }
    test_df = pd.DataFrame(raw_data)
    processed_json = process_data(test_df)
    processed_df = pd.read_json(processed_json)

    assert processed_df.isnull().sum().sum() == 0, "All NaN values should be dropped."

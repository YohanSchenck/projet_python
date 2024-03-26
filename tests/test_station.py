import pytest
from moulinette.station import request_station


def test_request_station_success(tmp_path):
    csv_data = "ID;Nom;Latitude;Longitude;Altitude\n1;Station1;50.0;5.0;100.0"
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(csv_data)

    data_json = request_station(csv_file)

    expected_json = '[{"station_id":1,"station_name":"Station1"}]'
    assert data_json == expected_json


def test_request_station_data_transform(tmp_path):
    csv_data = "ID;Nom;Latitude;Longitude;Altitude\n1;Station1;50.0;5.0;100.0"
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(csv_data)

    data_json = request_station(csv_file)

    expected_json = '[{"station_id":1,"station_name":"Station1"}]'
    assert data_json == expected_json


if __name__ == "__main__":
    pytest.main()

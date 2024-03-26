import json
import requests_mock
import pytest

from moulinette.upload import upload_meteo, upload_station


def test_upload_meteo_success():
    data_to_upload = {
        "station_id": 1,
        "year": 2021,
        "month": 5,
        "week": 20,
        "day": 140,
        "hour": 12,
        "temperature": 20.5,
        "wind": 10.5,
    }
    data_json = json.dumps(data_to_upload)

    # Simule une réponse réussie de l'API
    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:8000/upload/", text='{"success": true}', status_code=200
        )
        response = upload_meteo(data_json)

        assert response.status_code == 200
        assert response.json() == {"success": True}


def test_upload_meteo_failure():
    data_to_upload = {
        "station_id": 1,
        "year": 2021,
        "month": 5,
        "week": 20,
        "day": 140,
        "hour": 12,
        "temperature": 20.5,
        "wind": 10.5,
    }
    data_json = json.dumps(data_to_upload)

    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:8000/upload/",
            text='{"error": "Failed to upload data"}',
            status_code=500,
        )
        response = upload_meteo(data_json)

        assert response.status_code == 500
        assert response.json() == {"error": "Failed to upload data"}


def test_upload_station_success():
    station_data = {
        "ID": "Station1",
        "Name": "Someplace",
    }
    station_data_json = json.dumps(station_data)

    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:8000/upload_station/",
            text='{"success": true}',
            status_code=200,
        )
        response = upload_station(station_data_json)

        assert response.status_code == 200
        assert response.json() == {"success": True}


def test_upload_station_failure():
    station_data = {
        "ID": "Station1",
        "Name": "Someplace",
    }
    station_data_json = json.dumps(station_data)

    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:8000/upload_station/",
            text='{"error": "Failed to upload station data"}',
            status_code=500,
        )
        response = upload_station(station_data_json)

        assert response.status_code == 500
        assert response.json() == {"error": "Failed to upload station data"}


if __name__ == "__main__":
    pytest.main()

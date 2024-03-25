from fastapi.testclient import TestClient
from app.main import APP

client = TestClient(APP)


def test_read_main() -> None:
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_valid_upload_station() -> None:
    """Test the upload endpoint."""
    stations = [
        {
            "station_id": 1,
            "station_name": "test",
        }
    ]

    response = client.post("/upload_station/", json=stations)
    assert response.status_code == 200


def test_invalid_upload_station() -> None:
    """Test the upload endpoint."""
    stations = [
        {
            "station_id": 1,
            "station_name": 1,
        }
    ]

    response = client.post("/upload_station/", json=stations)
    assert response.status_code == 422


def test_valid_upload_meteo() -> None:
    """Test the upload endpoint."""
    meteos = [
        {
            "station_id": 89642,
            "year": 2000,
            "month": 1,
            "week": 5,
            "day": 31,
            "hour": 21,
            "temperature": -8.0,
            "wind": 9.7,
        }
    ]
    response = client.post("/upload_meteo/", json=meteos)
    assert response.status_code == 200


def test_invalid_upload() -> None:
    """Test the upload endpoint."""
    meteos = [
        {
            "station_id": "bjodokz",
            "year": 2000,
            "month": 1,
            "week": 5,
            "day": 31,
            "hour": 21,
            "temperature": -8.0,
            "wind": 9.7,
        }
    ]
    response = client.post("/upload_meteo/", json=meteos)
    assert response.status_code == 422

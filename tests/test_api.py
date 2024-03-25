from fastapi.testclient import TestClient
from app.main import APP

client = TestClient(APP)


def test_read_main() -> None:
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_valid_upload() -> None:
    """Test the upload endpoint."""
    meteos = [
        {
            "id": None,
            "station_id": 1,
            "year": 2021,
            "month": 1,
            "week": 1,
            "day": 1,
            "hour": 0,
            "wind": 1.0,
            "temperature": 1.0,
        }
    ]
    response = client.post("/upload/", json=meteos)
    assert response.status_code == 200
    print(response.json())
    assert response.json() == meteos


def test_invalid_upload() -> None:
    """Test the upload endpoint."""
    meteos = [
        {
            "station_id": "bojlz",
            "date": "2021-01-01T00:00:00",
            "wind": "bonjour",
            "temperature": 1.0,
        }
    ]
    response = client.post("/upload/", json=meteos)
    assert response.status_code == 422

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_main() -> None:
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_valid_upload() -> None:
    """Test the upload endpoint."""
    meteos = [
        {
            "station_id": 1,
            "date": "2021-01-01T00:00:00",
            "wind": 1.0,
            "temperature": 1.0,
        }
    ]
    response = client.post("/upload/", json=meteos)
    assert response.status_code == 200
    assert response.json() == meteos


def test_invalid_upload() -> None:
    """Test the upload endpoint."""
    meteos = [
        {
            "station_id": 1,
            "date": "2021-01-01T00:00:00",
            "wind": "bonjour",
            "temperature": 1.0,
        }
    ]
    response = client.post("/upload/", json=meteos)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "float_parsing",
                "loc": ["body", 0, "wind"],
                "msg": "Input should be a valid number, unable to parse string as a number",
                "input": "bonjour",
                "url": "https://errors.pydantic.dev/2.6/v/float_parsing",
            }
        ]
    }

from moulinette.upload import upload_data
import json


def test_upload_data():
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
    data = json.dumps(meteos)
    response = upload_data(data)
    assert (
        response.status_code == 200
    ), f"Expected 200 OK, got {response.status_code}: {response.text}"

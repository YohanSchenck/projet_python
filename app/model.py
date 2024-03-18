from typing import List
from pydantic import BaseModel


class MeteoIn(BaseModel):
    """Meteo data model."""

    station_id: int
    year: int
    month: int
    week: int
    day: int
    hour: int
    temperature: float
    wind: float


class Requested_data(BaseModel):
    rows: List[MeteoIn]

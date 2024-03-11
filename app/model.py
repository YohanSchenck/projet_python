from datetime import datetime
from pydantic import BaseModel


class Meteo(BaseModel):
    """Meteo data model."""

    station_id: int
    date: datetime
    wind: float
    temperature: float

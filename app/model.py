from typing import Optional
from sqlmodel import SQLModel, Field


class Meteo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    station_id: int
    year: int
    month: int
    week: int
    day: int
    hour: int
    wind: float
    temperature: float

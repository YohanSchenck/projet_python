from typing import Optional

from sqlmodel import Field, SQLModel


class Meteo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    station_id: int
    year: int
    month: int
    week: Optional[int] = None
    day: int
    hour: int
    wind: float
    temperature: float

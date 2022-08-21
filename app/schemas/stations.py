import datetime

from typing import List

from pydantic import BaseModel

from app.db.models import Line


class StationBase(BaseModel):
    name: str
    code: str
    lat: float = 0
    lon: float = 0
    lines: List[Line]
    timings: List[datetime.timedelta] = [datetime.timedelta(days=1)]


class StationCreate(StationBase):
    pass


class StationUpdate(StationBase):
    pass


class Station(StationBase):
    class Config:
        orm_mode = True

import datetime

from typing import List

from pydantic import BaseModel

from app.db.models.line import Line


class StationBase(BaseModel):
    name: str
    code: str
    id: int = -1
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


def get_station_by_name(stations: List[Station], name):
    return next(filter(lambda x: x["name"] == name, stations), None)


def get_station_by_id(stations: List[Station], id):
    return next(filter(lambda x: "id" in x and x["id"] == id, stations), None)

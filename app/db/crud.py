from typing import List

from sqlalchemy.orm import Session
from app.db.models.station import Station
from app.schemas.stations import StationCreate


def get_station(db: Session, station_code: str):
    return db.query(Station).filter(Station.code == station_code).first()


def get_stations(db: Session, offset: int = 0, limit: int = 100) -> List[Station]:
    return db.query(Station).offset(offset).limit(limit).all()


def create_station(db: Session, station: StationCreate):
    params = station.dict()
    params.update({"lines": ",".join(map(lambda x: str(x.value), params["lines"]))})
    db_station = Station(**params)

    db.add(db_station)
    db.commit()
    db.refresh(db_station)

    return db_station


# def update_station(db: Session, station_code: str):
#     db_station = get_station(db, Station.code == station_code)
#
#     db.add(db_station)
#     db.commit()
#     db.refresh(db_station)
#
#     return db_station
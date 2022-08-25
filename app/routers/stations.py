from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import stations
from app.db import crud
from app.db.SQLiteAdapter import get_db

router = APIRouter(
    tags=["stations"]
)


def init_lines():
    import json
    from app.schemas.stations import Line
    from app.db.crud import get_stations

    f = open('stations.json')
    data = json.load(f)
    line_data = data['lines']
    db = next(get_db())
    stations = get_stations(db)

    for station in stations:
        print(station)
        print(station.lines)

    for station in stations:
        station.lines = []
        for line in Line:
            if station.code in line_data[line.value]:
                station.lines.append(line)
        crud.update_station(db, station)

    # for line in Line:
    #     stations_in_line = data[line]
    #     if stations


# init_lines()


@router.get("/stations/", tags=["stations"], response_model=List[stations.Station])
async def list_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_stations(db, skip, limit)


@router.post("/stations/update", tags=["stations"])
async def update_stations():
    pass


@router.post("/stations/", tags=["stations"])
async def create_station(station: stations.StationCreate, db: Session = Depends(get_db)):
    db_station = crud.get_station(db, station.code)
    if db_station:
        raise HTTPException(status_code=400, detail="Station already exists")
    return crud.create_station(db, station)

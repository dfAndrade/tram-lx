from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import stations
from app.db import crud
from app.db.SQLiteAdapter import get_db

router = APIRouter(
    tags=["stations"]
)


@router.get("/stations/", tags=["stations"], response_model=List[stations.Station])
async def list_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stations = crud.get_stations(db, skip, limit)
    return stations


@router.post("/stations/update", tags=["stations"])
async def update_stations():
    pass


@router.post("/stations/", tags=["stations"])
async def create_station(station: stations.StationCreate, db: Session = Depends(get_db)):

    db_station = crud.get_station(db, station.code)
    if db_station:
        raise HTTPException(status_code=400, detail="Station already exists")
    return crud.create_station(db, station)

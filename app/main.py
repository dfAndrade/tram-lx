from fastapi import FastAPI

from app.db.models.station import Base
from app.db.SQLiteAdapter import engine
from app.routers import stations


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(stations.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

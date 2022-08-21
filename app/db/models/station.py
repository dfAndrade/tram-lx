from enum import Enum

from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import declarative_base

from app.db.decorators.lines import LineDecorator
from db.decorators.timings_decorator import TimingsDecorator

Base = declarative_base()


class Station(Base):
    __tablename__ = "stations"
    name = Column(String, index=True)
    code = Column(String, primary_key=True, unique=True, index=True)
    lat = Column(Numeric)
    lon = Column(Numeric)
    lines = Column(LineDecorator)
    timings = Column(TimingsDecorator)

    # def __repr__(self):
    #     return f'{self.name} ({self.code}) - {self.timings[0] if self.timings else "No trams available"}'

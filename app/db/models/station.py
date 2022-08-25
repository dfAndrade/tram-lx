from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from app.db.decorators.lines import LineDecorator
from app.db.decorators.timings_decorator import TimingsDecorator

Base = declarative_base()


class Station(Base):
    __tablename__ = "stations"
    name = Column(String, index=True)
    code = Column(String, primary_key=True, unique=True, index=True)
    id = Column(Integer)
    lat = Column(Numeric)
    lon = Column(Numeric)
    lines = Column(LineDecorator)
    timings = Column(TimingsDecorator)


class VirtualStation(Base):
    """
    Mocked station for diagram repr
    """

    __tablename__ = "v_stations"

    parent_code = Column(String, ForeignKey("stations.code"), primary_key=True, unique=True, index=True)
    lat = Column(Numeric)
    lon = Column(Numeric)

    # def __repr__(self):
    #     return f'{self.name} ({self.code}) - {self.timings[0] if self.timings else "No trams available"}'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Date
BaseModel = declarative_base()


class MarketEntry(BaseModel):
    __tablename__ = 'marketentry'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    iso_week = Column(String)
    symbol = Column(String)
    market = Column(String)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    market_cap = Column(Float)

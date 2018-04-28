from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
BaseModel = declarative_base()


class MarketEntry(BaseModel):
    __tablename__ = 'marketentry'

    id = Column(Integer, primary_key=True)

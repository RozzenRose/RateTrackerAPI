from app.database.engine import Base
from sqlalchemy import Column, func, DateTime, Float


class EthUsd(Base):
    __tablename__ = 'eth_usd'

    date_time = Column(DateTime, serever_default=func.now(), primary_key=True)
    rate = Column(Float)

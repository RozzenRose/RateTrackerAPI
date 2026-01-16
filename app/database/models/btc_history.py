from app.database.engine import Base
from sqlalchemy import Column, func, DateTime, Float


class BtcUsd(Base):
    __tablename__ = 'btc_usd'

    date_time = Column(DateTime(timezone=True), server_default=func.current_timestamp(), primary_key=True)
    rate = Column(Float)

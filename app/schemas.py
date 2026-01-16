from datetime import datetime, timedelta
from pydantic import BaseModel, model_validator, Field
from enum import Enum


class Currency(str, Enum): # сделам класс для валют
    btc = "btc"
    eth = "eth"


class TimeLimits(BaseModel): # валидация для временных интервалов
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError('Date error: start_date must be earlier than end_date')
        return self
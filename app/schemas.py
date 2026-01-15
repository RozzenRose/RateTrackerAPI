from datetime import datetime, timedelta
from pydantic import BaseModel, model_validator, Field
from enum import Enum


class Currency(str, Enum):
    btc = "btc"
    etc = "etc"


class TimeLimits(BaseModel):
    start_date: datetime = Field(default_factory=lambda: datetime.now() - timedelta(hours=1))
    end_date: datetime = Field(default_factory=datetime.now)

    @model_validator(mode='after')
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError('Date error: start_date must be earlier than end_date')
        return self
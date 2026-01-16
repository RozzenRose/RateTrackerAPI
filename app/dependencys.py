from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.schemas import TimeLimits
from datetime import datetime, timedelta


def time_limits_dep( # зависимость для временных интервалов
    start_date: datetime = datetime.now() - timedelta(hours=1),
    end_date: datetime = datetime.now(),
) -> TimeLimits:
    try:
        return TimeLimits(start_date=start_date,
                          end_date=end_date)
    except ValidationError as e:
        raise RequestValidationError(e.errors())

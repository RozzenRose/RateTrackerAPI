from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_depends import get_db
from app.database.db_functions.rates_db import (get_all_current_rates_form_db,
                                                get_last_current_rates_form_db,
                                                get_interval_rates_form_db)
from app.schemas import TimeLimits, Currency
from app.dependencys import time_limits_dep
from datetime import datetime


router = APIRouter(prefix='/rates', tags=['rates'])


@router.get('/all_current_rates')
async def get_all_current_rates(db: Annotated[AsyncSession, Depends(get_db)],
                                currency: Currency = Currency.btc):
    answer = await get_all_current_rates_form_db(db, currency)
    return {'answer': answer}


@router.get('/last_current_rates')
async def get_last_current_rates(db: Annotated[AsyncSession, Depends(get_db)],
                                 currency: Currency = Currency.btc):
    answer = await get_last_current_rates_form_db(db, currency)
    return {'answer': answer}


@router.get('/interval_rates')
async def get_interval_rates(db: Annotated[AsyncSession, Depends(get_db)],
                             currency: Currency = Currency.btc,
                             time_limits: TimeLimits = Depends(time_limits_dep)):
    answer = await get_interval_rates_form_db(db, currency, time_limits)
    print(answer)
    if answer == []:
        return {'answer': 'No data found'}
    return {'answer': answer}